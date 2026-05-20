from dataclasses import dataclass
from typing import Any, List, Dict, Callable
from mlx_lm.sample_utils import make_sampler
from mlx_lm import generate
from copy import deepcopy

from razomy.ai_hugging_face.chat.logic.predict import models
from razomy.cache.registry import global_cache_registry
from razomy.ai_hugging_face.chat.log import universal_log
from razomy.ai_hugging_face.chat.predict import AIContext, create_chat_model, Opt


@universal_log('Predict')
def predict_ctx(ctx: AIContext, messages: List[Dict], tools_spec: List[Any] = None) -> dict[str, str] | Any:
    prompt = ctx.tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False,
        enable_thinking=False,
        tools=tools_spec,
    )

    response = predict_string(ctx, prompt, None)

    start_tool = response.find(ctx.tokenizer.tool_call_start)
    end_tool = response.find(ctx.tokenizer.tool_call_end)
    if start_tool != -1 and end_tool != -1:
        start_tool_offset = start_tool + + len(ctx.tokenizer.tool_call_start)
        tool_call = ctx.tokenizer.tool_parser(response[start_tool_offset:end_tool].strip())
        return {"role": "call", "content": tool_call}

    return {"role": "assistant", "content": response}


def print_prompt(prompt):
    class c:
        # Базовые модификаторы
        RESET = '\033[0m'
        BOLD = '\033[1m'

        # Палитра 256 цветов (ВЫСОКИЙ КОНТРАСТ для БЕЛОГО фона)
        GRAY_SYSTEM = '\033[38;5;238m'  # Темно-серый (Системные промпты)
        GRAY_BOUND = '\033[38;5;244m'  # Средне-серый (Границы токенов)
        BLUE = '\033[38;5;25m'  # Глубокий синий (Пользователь)
        PURPLE = '\033[38;5;90m'  # Темно-фиолетовый (Модель)
        ORANGE = '\033[38;5;130m'  # Жженая бронза/Кирпичный (Инструменты)
        GREEN = '\033[38;5;28m'  # Темно-зеленый (Ответ инструментов)
        TEAL = '\033[38;5;30m'  # Глубокий изумрудный/Teal (Размышления)
        BROWN = '\033[38;5;94m'  # Темно-коричневый (Контекст/RAG)
        RED = '\033[38;5;124m'  # Темно-красный (Ошибки)

    prnt = prompt

    # Словарь всех возможных тегов
    tags_colors = {
        # 1. Основные роли
        '<|turn>system': c.GRAY_SYSTEM,
        '<|turn>user': c.BLUE,
        '<|turn>model': c.PURPLE,

        # 2. Работа с инструментами (Function Calling)
        '<|turn>tool': c.ORANGE,
        '<|tool_call>call': c.BROWN,
        '<|tool_response>response': c.GREEN,
    }

    # Применяем цвета (Тег будет жирным и цветным)
    for tag, color in tags_colors.items():
        # Заменяем тег на его цветную версию
        prnt = prnt.replace(tag, f"{c.BOLD}{color}{tag}{c.RESET}")

    print(prnt)


@universal_log('Predict')
def predict_string(ctx: AIContext, prompt: str, opts = None) -> str:
    if opts is None:
        opts = Opt()
    else:
        opts = Opt(**opts)

    if opts.update_cache:
        temp_cache = ctx.cache
    else:
        temp_cache = deepcopy(ctx.cache)

    if opts.verbose:
        print('Request:---')
        print_prompt(prompt)
        print('Model:---')

    sampler = make_sampler(
        temp=opts.temperature,  # ВАЖНО: Убираем 0.0! Ставим 0.6 - 0.8. Это добавит случайности.
        top_p=0.95,  # Ограничиваем "хвост" бредовых токенов.
        min_p=0.05,  # Альтернатива top_p, отсекает слова с вероятностью ниже 5% от лучшего.
        top_k=64,
        # --- СЕКРЕТНОЕ ОРУЖИЕ MLX ОТ ЗАЦИКЛИВАНИЯ ---
        xtc_probability=0.15,  # С вероятностью 15% модель ПРИНУДИТЕЛЬНО проигнорирует самый частый токен.
        xtc_threshold=0.1  # Применяется только если токен имеет вероятность выше 10%.
    )

    response = generate(
        model=ctx.model,
        tokenizer=ctx.tokenizer,
        prompt=prompt,
        sampler=sampler,
        max_tokens=opts.max_tokens,
        verbose=opts.verbose,
        prompt_cache=temp_cache
    )

    # if opts['verbose']:
    #     print('---s')
    #     print(response)
    #     print('---e')
    return response


def predict(model_id, messages, tools_spec: List[Any] = None):
    ctx = create_chat_model(model_id)
    return predict_ctx(ctx, messages, tools_spec)


def predict_cache_string(cache_id, model_id, text, opts=None):
    cache_id, ctx = global_cache_registry.get_or_put(cache_id, lambda: create_chat_model(model_id))
    response = predict_string(ctx, text, opts)
    return cache_id, response


def cache_predict(cache_id, model_id, messages, tools_spec: List[Any] = None):
    cache_id, ctx = global_cache_registry.get_or_put(cache_id, lambda: create_chat_model(model_id))
    response = predict_ctx(ctx, messages, tools_spec)
    return cache_id, response


def try_call_tool(ai: AIContext, messages, tools):
    if messages[-1]['role'] == 'call':
        response = messages[-1]["content"]
        tool_result = tools[response["name"]](**response["arguments"])
        return {
            "role": "assistant",
            "tool_calls": [{"function": {"name": response["name"], "arguments": response.get("arguments", {})}}],
            "tool_responses": [{"name": response["name"], "response": tool_result}],
            "content": ""
        }
    return None


def try_message_tool_mut(ctx: AIContext, messages: List[Dict], tools: Dict[str, Callable]) -> bool:
    res = try_call_tool(ctx, messages, tools)
    if res:
        messages[-1] = res
        return True
    return False


def test_predict():
    model_id = models['2_4']

    def multiply(a: float, b: float):
        """
        A function that multiplies two numbers

        Args:
            a: The first number to multiply
            b: The second number to multiply
        """
        return a * b

    tools = {"multiply": multiply}
    tools_list = list(tools.values())

    prompt = "Multiply 12234585 and 48838483920. And say answer."
    messages = [{"role": "user", "content": prompt}]
    response = predict(model_id, messages, tools_list)
    print(response)


def test_predict_ctx():
    model_id = models['2_4']
    ctx = create_chat_model(model_id)

    def multiply(a: float, b: float):
        """
        A function that multiplies two numbers

        Args:
            a: The first number to multiply
            b: The second number to multiply
        """
        return a * b

    tools = {"multiply": multiply}
    tools_list = list(tools.values())

    prompt = "Multiply 12234585 and 48838483920. And say answer."
    messages = [{"role": "user", "content": prompt}]
    response = predict_ctx(ctx, messages, tools_list)
    print(response)
    messages.append(response)
    try_message_tool_mut(ctx, messages, tools)
    response = predict_ctx(ctx, messages, tools_list)
    print(response)


def test_cache_predict_text():
    tools_spec = [{
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "A function that multiplies two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number to multiply"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number to multiply"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }]
    messages = [{"role": "user", "content": "Multiply 12234585 and 48838483920. And say answer."}]
    print(cache_predict("1", models['2_4'], messages, tools_spec))


def test_predict_cache_string():
    cache_id = "1"
    prompt = """
<bos><|turn>system
<|tool>declaration:multiply{description:<|"|>A function that multiplies two numbers<|"|>,parameters:{properties:{a:{description:<|"|>The first number to multiply<|"|>,type:<|"|>NUMBER<|"|>},b:{description:<|"|>The second number to multiply<|"|>,type:<|"|>NUMBER<|"|>}},required:[<|"|>a<|"|>,<|"|>b<|"|>],type:<|"|>OBJECT<|"|>}}<tool|><turn|>
<|turn>user
Multiply 12234585 and 48838483920. And say answer.<turn|>
<|turn>model
    """.strip()
    cache_id, result = predict_cache_string(cache_id, models['2_4'], prompt,
                                            {"verbose": True, "update_cache": True, "max_tokens": 500})
    prompt += result
    prompt += '<|tool_response>response:multiply{value:597518582790373200}<tool_response|>'
    cache_id, result = predict_cache_string(cache_id, models['2_4'], prompt,
                                            {"verbose": True, "update_cache": True, "max_tokens": 500})
    prompt += result
    print(prompt)
