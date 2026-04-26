from copy import deepcopy

from mlx_lm import generate, stream_generate
from mlx_lm.sample_utils import make_sampler
from razomy.cache.registry import global_cache_registry
from razomy.ai_hugging_face.chat.log import request_log
from razomy.ai_hugging_face.chat.predict import cache_load, AIContext, create_chat_model
from typing import Iterator, Dict, Any

# doc https://ai.google.dev/gemma/docs/capabilities/thinking
models = {
    # '31_16': 'mlx-community/gemma-4-31b-it-bf16', too large for this mac
    '31_8': 'mlx-community/gemma-4-31b-it-8bit',
    '31_4': 'mlx-community/gemma-4-31b-it-4bit',
    # '26_4': 'mlx-community/gemma-4-26b-a4b-4bit', run error
    '4_8': 'mlx-community/gemma-4-e4b-it-8bit',
    '4_4': 'mlx-community/gemma-4-e4b-it-4bit',
    '2_4': 'mlx-community/gemma-4-e2b-it-4bit'
}


# --- Modified predict_ctx for Streaming ---
@request_log
def predict_ctx_stream(ctx, messages) -> Iterator[Dict[str, str]]:
    model, tokenizer = (ctx.model, ctx.tokenizer)

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )
    sampler = make_sampler(
        temp=0.9,  # ВАЖНО: Убираем 0.0! Ставим 0.6 - 0.8. Это добавит случайности.
        top_p=0.95,  # Ограничиваем "хвост" бредовых токенов.
        min_p=0.05,  # Альтернатива top_p, отсекает слова с вероятностью ниже 5% от лучшего.
        top_k=64,
        # --- СЕКРЕТНОЕ ОРУЖИЕ MLX ОТ ЗАЦИКЛИВАНИЯ ---
        xtc_probability=0.15,  # С вероятностью 15% модель ПРИНУДИТЕЛЬНО проигнорирует самый частый токен.
        xtc_threshold=0.1  # Применяется только если токен имеет вероятность выше 10%.
    )

    stream = stream_generate(
        model,
        tokenizer,
        prompt=prompt,
        sampler=sampler,
        max_tokens=65536,
    )

    for chunk in stream:
        content = chunk.text
        yield {"role": "assistant", "content": content}


@request_log
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

def cache_predict_stream(cache_id: str, model_id: str, messages: list) -> Iterator[Dict[str, str]]:
    cache_id, ctx = global_cache_registry.get_or_put(cache_id, lambda: create_chat_model(model_id))
    return predict_ctx_stream(ctx, messages)

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
