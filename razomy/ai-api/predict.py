import os
from mlx_vlm import load, generate

models = {
    'expensive': 'mlx-community/gemma-4-31b-it-4bit',
    'cheapest': 'mlx-community/gemma-4-e2b-it-4bit'
}
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
MODEL_ID = models.get('cheapest')

print("⏳ Загрузка процессора и модели (это займет некоторое время)...")
model, processor = load(MODEL_ID)
print("✅ Модель успешно загружена и готова к работе!")

def predict(messages) -> str:
    prompt_text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    outputs = generate(
        model,
        processor,
        prompt=prompt_text,
        max_tokens=65536,
        temperature=1.0,
        top_p=0.95,
        top_k=64,
    )

    return outputs.text
