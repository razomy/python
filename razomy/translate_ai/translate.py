from razomy.ai_hugging_face.chat.predict import cache_load, predict

models = {
    '4_4': 'mlx-community/translategemma-4b-it-4bit',
    '27_16': 'mlx-community/translategemma-27b-it-bf16',
    '27_4': 'mlx-community/translategemma-27b-it-4bit'
}

def translate(text: str, from_locale: str, to_locale: str, glossary: dict = None):
    final_text_prompt = text

    if glossary:
        glossary_rules = "\n".join([f"- '{k}' translate as '{v}'" for k, v in glossary.items()])
        final_text_prompt = (
            f"Translate the text strictly following this glossary:\n"
            f"{glossary_rules}\n\n"
            f"Text:\n{text}"
        )

    # 2. Передаем в модель
    res = predict(
        models['4_4'],
        [
            {
                "role": "user",
                'content': [
                    {
                        "type": "text",
                        'source_lang_code': from_locale,
                        'target_lang_code': to_locale,
                        'text': final_text_prompt  # Используем наш модифицированный текст
                    }
                ]
            }
        ],
        {}
    )['content']

    # 3. Очистка результата (ваша логика)
    stops = ["<end_of_turn>", "<eos>", "<pad>"]
    for stop in stops:
        if stop in res:
            res = res.split(stop)[0]

    res = (res
           .replace('<end_of_turn>', '')
           .strip()
           .removeprefix("**")
           .removesuffix("**")
           .strip()
           )
    return res


def test_translate():
    # Пример 1: Обычный перевод
    data = translate( "I like Apple products.", "en", "ru")
    print(data)
    # Выдаст: "Мне нравятся продукты Apple." или "Мне нравятся яблочные продукты."

    # Пример 2: Использование глоссария
    my_glossary = {
        "Apple": "Компания Эппл",
        "products": "устройства"
    }

    print(translate("I like Apple products.", "en", "ru", glossary=my_glossary))
