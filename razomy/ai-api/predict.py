import os
from mlx_vlm import load, generate

from mlx_vlm.prompt_utils import apply_chat_template

models = {
    '31_4': 'mlx-community/gemma-4-31b-it-4bit',
    '26_4': 'mlx-community/gemma-4-26b-a4b-4bit',
    '4_8': 'mlx-community/gemma-4-e4b-it-8bit',
    '4_4': 'mlx-community/gemma-4-e4b-it-4bit',
    '2_4': 'mlx-community/gemma-4-e2b-it-4bit'
}
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
MODEL_ID = models.get('4_8')

print("⏳ Загрузка процессора и модели (это займет некоторое время)...")
model, processor = load(MODEL_ID)
print("✅ Модель успешно загружена и готова к работе!")

def predict(messages) -> str:
    prompt = apply_chat_template(
        processor,
        model.config,
        prompt=messages,
        tokenize=False,
    )

    outputs = generate(
        model,
        processor,
        prompt=prompt,
        max_tokens=65536,
        temperature=1.0,
        top_p=0.95,
        top_k=64,
    )

    return outputs.text
