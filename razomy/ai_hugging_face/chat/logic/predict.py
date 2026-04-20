from mlx_lm import generate
from mlx_lm.sample_utils import make_sampler
from razomy.cache.registry import global_cache_registry
from razomy.ai_hugging_face.chat.log import request_log
from razomy.ai_hugging_face.chat.predict import cache_load, AIContext, create_chat_model

models = {
    '31_4': 'mlx-community/gemma-4-31b-it-4bit',
    '26_4': 'mlx-community/gemma-4-26b-a4b-4bit',
    '4_8': 'mlx-community/gemma-4-e4b-it-8bit',
    '4_4': 'mlx-community/gemma-4-e4b-it-4bit',
    '2_4': 'mlx-community/gemma-4-e2b-it-4bit'
}

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

def test_predict():
    print(predict(models['2_4'], [{'role': 'user', 'content': 'hello'}]))

def test_cache_predict():
    print(cache_predict("1", models['2_4'], [{'role': 'user', 'content': 'hello'}]))
