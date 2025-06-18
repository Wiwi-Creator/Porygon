import json
import requests


payload = json.dumps({
    "inputs": [{"input": "Tell a joke!"}]  # 修改為正確的格式
})

response = requests.post(
    url="http://127.0.0.1:5000/invocations",
    data=payload,
    headers={"Content-Type": "application/json"},
)
print(response.json())
