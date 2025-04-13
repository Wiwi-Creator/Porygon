import json
import requests

# base url
base_url = "http://localhost:9999"

# health check
#health_response = requests.get(f"{base_url}/health")
#print(f"Health Check: {health_response.json()}")

# chat_check
payload = json.dumps({
    "inputs": [{"input": "Tell a joke!"}]  # 修改為正確的格式
})

response = requests.post(
    url=f"{base_url}/predict",
    data=payload,
    headers={"Content-Type": "application/json"}
)
print(response.json())
