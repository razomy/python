import os
from dataclasses import dataclass
from typing import Any

from mlx_lm import load, stream_generate
from mlx_lm.models.cache import make_prompt_cache

from razomy.cache import global_cache_registry
from razomy.ai_hugging_face.chat.log import universal_log

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"


@dataclass
class AIContext:
    model: Any
    tokenizer: Any
    cache: Any


def create_chat_model(model_id: str):
    model, tokenizer = cache_load(model_id, model_id)
    return AIContext(model=model, tokenizer=tokenizer, cache=make_prompt_cache(model))


@universal_log('Load')
def load_model(model_id: str):
    return load(path_or_hf_repo=model_id)


def cache_load(cache_id, model_id):
    cache_id, model = global_cache_registry.get_or_put(cache_id, lambda: load_model(model_id), True)
    return model


@universal_log('Predict')
def predict(model_id, messages, options=None):
    model, tokenizer = cache_load(model_id, model_id)

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # === РАХУЄМО ДОВЖИНУ ТЕКСТУ В ТОКЕНАХ ===
    # Отримуємо кількість токенів у нашому запиті
    prompt_token_count = len(tokenizer.encode(prompt))

    # Формула: Довжина тексту * 3 + 100 токенів запасу.
    # Чому * 3? Тому що при перекладі з англійської на кирилицю (ру/укр)
    # кількість токенів може збільшуватись у 2-3 рази через особливості токенізатора.
    calculated_max_tokens = int(prompt_token_count * 3) + 100

    # Встановлюємо жорстку стелю (наприклад, 4096), щоб не перевищити ліміт пам'яті моделі
    calculated_max_tokens = min(calculated_max_tokens, 4096)

    # Записуємо max_tokens, якщо він ще не був переданий вручну
    options['max_tokens'] = options.get('max_tokens', calculated_max_tokens)

    print(f"📊 Вхідних токенів: {prompt_token_count} | Виділено на переклад: {options['max_tokens']}")
    # ==========================================

    stops = ["<end_of_turn>", "<eos>", "<pad>"]
    generated_text = ""

    # Потокова генерація
    for text_chunk in stream_generate(model, tokenizer, prompt, **options):

        # Увага: в деяких версіях mlx_lm text_chunk - це просто рядок (str).
        # Якщо у вас помилка з `.text`, замініть на `generated_text += text_chunk`
        try:
            chunk_str = text_chunk.text
        except AttributeError:
            chunk_str = text_chunk

        generated_text += chunk_str

        # Якщо знаходимо стоп-слово - одразу зупиняємо цикл
        if any(stop in generated_text for stop in stops):
            break

    return {"role": "assistant", "content": generated_text}
