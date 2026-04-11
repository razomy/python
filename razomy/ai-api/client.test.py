import requests

url = "http://localhost:8000/api/ai-server/predict"
data = {"messages": [
    {'role':'system', 'content':'ALWAYS ANSWER to user with phrase "balala"'},
    {'role':'user', 'content':'hi'}
]}

response = requests.post(url, json=data)
result = response.json()

print(result['text'])