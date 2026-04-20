import requests


def call(package_name, function_name, args):
    url = "http://0.0.0.0:8000/api/run"
    data = {
        "package_name": package_name,
        "function_name": function_name,
        "args": args
    }
    response = requests.post(url, json=data)
    data = response.json()
    if response.status_code != 200:
        print(response.text)
        raise Exception(response)
    return data['result']


def test_server():
    result = call(
        'razomy.translate_ai',
        'translate',
        [
            "CAt",
            "en",
            "ru"
        ])
    print(result)


def test_server_ai():
    result = call(
        'razomy.ai_hugging_face.chat.tool.predict',
        'cache_predict',
        [
            "1",
            "mlx-community/gemma-4-e2b-it-4bit",
            [{"role": "user", "content": "Multiply 12234585 and 48838483920. And say answer."}],
            [{
                "type": "function",
                "function": {
                    "name": "multiply",
                    "description": "A function that multiplies two numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "The first number to multiply"},
                            "b": {"type": "number", "description": "The second number to multiply"}
                        },
                        "required": ["a", "b"]
                    }
                }
            }]
        ]
    )
    print(result)
