import queue
import threading
from copy import deepcopy
from dataclasses import asdict

from mlx_lm import generate, stream_generate
from mlx_lm.sample_utils import make_sampler
from pyarrow.lib import Queue

from razomy.cache.registry import global_cache_registry
from razomy.ai_huggingface.chat.log import universal_log, universal_log
from razomy.ai_huggingface.chat.predict import cache_load, AIContext, create_chat_model, Opt
from typing import Iterator, Dict, Any
import multiprocessing
import signal

# doc https://ai.google.dev/gemma/docs/capabilities/thinking
models = {
    # 'qwen38_16': 'mlx-community/Qwen3.8-27B-bf16',
    'qwen38_8': 'mlx-community/Qwen3.8-27B-8bit',
    'qwen38_4': 'mlx-community/Qwen3.8-27B-4bit',
    # '31_16': 'mlx-community/gemma-4-31b-it-bf16',# too large for this mac
    '31_8': 'mlx-community/gemma-4-31b-it-8bit',
    '31_4': 'mlx-community/gemma-4-31b-it-4bit',
    # '26_4': 'mlx-community/gemma-4-26b-a4b-4bit', run error
    '4_8': 'mlx-community/gemma-4-e4b-it-8bit',
    '4_4': 'mlx-community/gemma-4-e4b-it-4bit',
    '2_4': 'mlx-community/gemma-4-e2b-it-4bit'
}


# --- Modified predict_ctx for Streaming ---
@universal_log('Predict')
def predict_ctx_stream(ctx, messages, opts=None) -> Iterator[Dict[str, str]]:
    if opts is None:
        opts = Opt()
    else:
        opts = Opt(**opts)
    model, tokenizer = (ctx.model, ctx.tokenizer)

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )
    sampler = make_sampler(
        temp=opts.temperature,  # ВАЖНО: Убираем 0.0! Ставим 0.6 - 0.8. Это добавит случайности.
        top_p=0.95,  # Ограничиваем "хвост" бредовых токенов.
        min_p=0.05,  # Альтернатива top_p, отсекает слова с вероятностью ниже 5% от лучшего.
        top_k=64,
        # --- СЕКРЕТНОЕ ОРУЖИЕ MLX ОТ ЗАЦИКЛИВАНИЯ ---
        xtc_probability=0.15,  # С вероятностью 15% модель ПРИНУДИТЕЛЬНО проигнорирует самый частый токен.
        xtc_threshold=0.1  # Применяется только если токен имеет вероятность выше 10%.
    )
    if opts.update_cache:
        temp_cache = ctx.cache
    else:
        temp_cache = deepcopy(ctx.cache)

    stream = stream_generate(
        model,
        tokenizer,
        prompt=prompt,
        sampler=sampler,
        max_tokens=opts.max_tokens,
        prompt_cache=temp_cache,
    )

    for chunk in stream:
        content = chunk.text
        yield {"role": "assistant", "content": content}


@universal_log('Predict')
def predict_ctx(ctx, messages):
    model, tokenizer = (ctx.model, ctx.tokenizer)

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )
    sampler = make_sampler(
        temp=1.0,
        top_p=0.95,
        top_k=64,
    )
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        sampler=sampler,
        max_tokens=65536,
    )
    return {"role": "assistant", "content": response}


def predict(model_id, messages):
    ctx = create_chat_model(model_id)
    return predict_ctx(ctx, messages)


def cache_predict(cache_id, model_id, messages):
    cache_id, ctx = global_cache_registry.get_or_put(cache_id, lambda: create_chat_model(model_id))
    response = predict_ctx(ctx, messages)
    return cache_id, response


def cache_copy(cache_id, new_cache_id):
    cache_id, ctx = global_cache_registry.get[AIContext](cache_id, cache_id)
    new_ctx = AIContext(model=ctx.model, tokenizer=ctx.tokenizer, cache=deepcopy(ctx.cache))
    new_cache_id = global_cache_registry.put(new_cache_id, new_ctx)
    return new_cache_id


def cache_predict_stream(cache_id: str, model_id: str, messages: list, opts=None) -> Iterator[Dict[str, str]]:
    cache_id, ctx = global_cache_registry.get_or_put(cache_id, lambda: create_chat_model(model_id))
    return predict_ctx_stream(ctx, messages, opts)


def get_prev_report_and_to_compress(messages):
    last_summary_idx = -1
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].get('is_summary'):
            last_summary_idx = i
            break

            # 2. Separate the existing summary from the new content
    previous_summary = {
            "role": "system",
            "content": f"",
            "is_summary": True
        }
    if last_summary_idx != -1:
        previous_summary["content"] = messages[last_summary_idx].get('content', '')
        # Everything AFTER the last summary needs to be processed
        to_summarize_messages = messages[last_summary_idx + 1:]
    else:
        # No summary found, process everything
        to_summarize_messages = messages
    return previous_summary, to_summarize_messages


def compress_history(chat_id, model_id, new_history_text, fn) -> str:
    init_summary_prompt = (
        f"Perform a high-fidelity extraction of facts and context from the following conversation. "
        f"Avoid over-generalization and 'averaging' the content. "
        f"Instead, identify and preserve:\n"
        f"- Specific nuances, subtle requirements, and unique constraints and logic.\n"
        f"- Key pivot points in the conversation (where the direction or opinion changed).\n"
        f"- Explicit and implicit commitments or concerns.\n"
        f"- Any specific terminology or phrasing used by the participants that carries weight.\n"
        f"- Add Completely final code and complex logic.\n\n"
        f"Requirements:\n"
        f"- Be granular: prefer multiple specific points over one vague general statement.\n"
        f"- Do not omit details for the sake of brevity if those details are critical to the meaning.\n"
        f"- Use direct quotes for nuanced expressions to avoid loss of meaning.\n\n"
    )

    # INITIAL MODE: Create the first summary
    summary_prompt = (
            init_summary_prompt +
            f"CONVERSATION:\n{new_history_text}"
    )

    temp_messages = [{"role": "user", "content": summary_prompt}]
    s = fn(chat_id, model_id, temp_messages, asdict(Opt(temperature=.4)))

    res = ''
    for chunk in s:
        content = chunk.get('content', '')
        if content:
            res += content
    return res


def unite_history(chat_id, model_id, previous_summary, compressed, fn) -> str:
    summary_prompt = (
        f"You are a memory management system.\n"
        "Merge the 'Existing Report' with the 'New Report' details and return it as single report.\n"
        f"1. Merge new facts into the existing storage while maintaining a granular, bulleted format.\n"
        f"2. Update existing points if the user has changed their mind or requirements (pivot points).\n"
        f"3. Preserve specific nuances, terminology, direct quotes, and nuanced requirements.\n"
        f"4. Key Preserve pivot points in the conversation (where the direction or opinion changed).\n"
        f"5. Explicit and implicit commitments or concerns.\n"
        f"6. Update final version code(context) and complex logic.\n"
        f"7. Remove redundant details that are no longer relevant, but keep critical constraints.\n"
        f"8. Do not summarize; provide the full, updated state of facts."
        f"EXISTING REPORT:\n{previous_summary}\n\n"
        f"NEW REPORT:\n{compressed}\n\n"
    )

    temp_messages = [{"role": "user", "content": summary_prompt}]
    s = fn(chat_id, model_id, temp_messages, asdict(Opt(temperature=.4)))

    res = ''
    for chunk in s:
        content = chunk.get('content', '')
        if content:
            res += content
    return res


def summarize_history(chat_id, model_id, messages, fn):
    previous_summary, to_summarize_messages = get_prev_report_and_to_compress(messages)

    if not to_summarize_messages:
        return previous_summary

        # Format new messages into a block
    new_history_text = "\n".join([f"{m['role']}: {m['content']}" for m in to_summarize_messages])
    compressed = compress_history(chat_id, model_id, new_history_text, fn)

    if not previous_summary["content"]:
        return {
            "role": "system",
            "content": f"{compressed}",
            "is_summary": True
        }
    unied = unite_history(chat_id, model_id, previous_summary["content"], compressed, fn)
    return {
        "role": "system",
        "content": f"{unied}",
        "is_summary": True
    }


class BackgroundStreamWorker:
    def __init__(self, generator_func, use_multiprocessing=True):
        self.generator_func = generator_func
        self.cmd_queue = multiprocessing.Queue()
        self.res_queue = multiprocessing.Queue()
        # Создаем флаг отмены
        self.abort_event = multiprocessing.Event()

        if use_multiprocessing:
            # Создаем отдельный процесс (изолированная память, свой GIL)
            self.process = multiprocessing.Process(
                target=self._worker_loop,
                args=(generator_func, self.cmd_queue, self.res_queue, self.abort_event)
            )
            print("Запущено в отдельном процессе")
        else:
            # Создаем поток (общая память, общий GIL)
            self.process = threading.Thread(
                target=self._worker_loop,
                args=(generator_func, self.cmd_queue, self.res_queue, self.abort_event)
            )
            print("Запущено в потоке (текущий процесс)")

        self.process.start()

    def clear_cache(self, chat_id):
        self.cmd_queue.put({"type": "CLEAR_CACHE", "chat_id": chat_id})

    @staticmethod
    def _worker_loop(generator_func, cmd_queue: Queue, res_queue: Queue, abort_event):
        # Воркер полностью игнорирует системный Ctrl+C, он слушает только наши команды
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        while True:
            job = cmd_queue.get()
            if job == "STOP":
                break
            # Проверяем, не команда ли это на очистку
            if isinstance(job, dict) and job.get("type") == "CLEAR_CACHE":
                chat_id = job.get("chat_id")
                global_cache_registry.delete(chat_id)
                continue
            args, kwargs = job

            try:
                # Создаем объект-генератор
                gen = generator_func(*args, **kwargs)

                # Итерируемся по нему
                for chunk in gen:
                    # На каждом шаге проверяем флаг отмены от главного процесса!
                    if abort_event.is_set():
                        # print("\n🛑 [Рабочий процесс] Получен сигнал отмены! Закрываем генератор...")
                        gen.close()  # Безопасно завершаем работу генератора
                        break  # Выходим из цикла выдачи

                    res_queue.put(chunk)

            except Exception as e:
                res_queue.put(e)

            # Обязательно кидаем маркер завершения (и при успехе, и при отмене)
            res_queue.put(StopIteration)

    def __call__(self, *args, **kwargs):
        # 1. Перед новым запуском опускаем флаг отмены
        self.abort_event.clear()

        # 2. Очищаем очередь от мусора (если что-то застряло с прошлого раза)
        while not self.res_queue.empty():
            try:
                self.res_queue.get_nowait()
            except queue.Empty:
                break

        # 3. Отправляем команду воркеру
        self.cmd_queue.put((args, kwargs))

        try:
            while True:
                try:
                    chunk = self.res_queue.get(timeout=0.1)
                    if chunk is StopIteration:
                        break
                    if isinstance(chunk, Exception):
                        raise chunk
                    yield chunk

                except queue.Empty:
                    if not self.process.is_alive():
                        raise RuntimeError("Фоновый процесс внезапно умер (возможно OOM Killer)!")

        except KeyboardInterrupt:
            # ==========================================
            # ЕСЛИ ПОЛЬЗОВАТЕЛЬ НАЖАЛ CTRL+C
            # ==========================================
            # print("\n⚠️ Прерываем текущий стрим...")

            # Поднимаем флаг! Воркер увидит его на следующем yield и остановится.
            self.abort_event.set()

            # ОЧЕНЬ ВАЖНО: Мы должны вытаскивать все остатки из очереди,
            # пока не встретим StopIteration. Это гарантирует, что воркер
            # точно остановился и готов к следующему вызову.
            while True:
                try:
                    junk = self.res_queue.get(timeout=0.5)
                    if junk is StopIteration:
                        break  # Воркер подтвердил остановку!
                except queue.Empty:
                    pass

            raise  # Прокидываем KeyboardInterrupt дальше, чтобы остановить ваш код

    def close(self):
        if self.process.is_alive():
            self.cmd_queue.put("STOP")
            self.process.join()


def test_predict():
    print("\n--- Testing Non-Streaming Predict ---")
    result = predict(models['2_4'], [{'role': 'user', 'content': """                                                                                                            
hello                                                                                                                                                                           
"""}])
    print(result['content'])


def test_cache_predict():
    print("\n--- Testing Cached Predict (Sync) ---")
    cache_id, response = cache_predict("1", models['2_4'], [{'role': 'user', 'content': 'hello'}])
    print(f"Cache ID: {cache_id}")
    print("Response:", response['content'])


def test_cache_predict_stream():
    print("\n--- Testing Cached Predict (Stream) ---")
    # Since this returns an iterator, we need to consume it
    print("Streaming response:")
    stream_iterator = cache_predict_stream("2", models['2_4'],
                                           [{'role': 'user', 'content': 'Write a short story about a space cat.'}])

    full_response = ""
    for chunk in stream_iterator:
        print(chunk['content'], end="", flush=True)
        full_response += chunk['content']
    print("\n--- Stream End ---")
