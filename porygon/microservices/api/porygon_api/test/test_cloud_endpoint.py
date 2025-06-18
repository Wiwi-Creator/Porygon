import requests
import json


#base_url = "https://porygon-api-931091704211.asia-east1.run.app"
base_url = "http://localhost:9999"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "admin_key"
}


def query_wikipedia_agent():
    """向 Wikipedia Agent 發送查詢"""
    url = f"{base_url}/api/v1/porygon/AIservice/wikipedia_agent"
    payload = {"query": "Who is the biggest Pokemon?"}

    response = requests.post(url, headers=headers, json=payload)
    print("Status code:", response.status_code)
    print("result:", json.dumps(response.json(), indent=2))
    return response.json()


def get_metrics(date="2025-04-20"):
    """獲取指定日期的指標"""
    url = f"{base_url}/metric?date={date}"

    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)
    print("Metric:", json.dumps(response.json(), indent=2))
    return response.json()


def check_health():
    """檢查服務健康狀態"""
    url = f"{base_url}/health"

    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)
    print("Status:", json.dumps(response.json(), indent=2))
    return response.json()


def get_item(item_id="bcc4f2ff-1b65-4e28-b2bb-b0475fab73a2"):
    """從 Cloud SQL 獲取物品"""
    url = f"{base_url}/api/v1/porygon/UserQuery/resource/GetItems/{item_id}"

    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)
    print("Iytem Detail:", json.dumps(response.json(), indent=2))
    return response.json()


def get_product(collection="Product", product_id="A123"):
    """從 Firestore 獲取產品"""
    url = f"{base_url}/api/v1/porygon/UserQuery/resource/GetProducts/{collection}/{product_id}"

    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)
    print("Product detail:", json.dumps(response.json(), indent=2))
    return response.json()


#print("執行 Wikipedia Agent 查詢...")
#query_wikipedia_agent()
print("\n獲取指標數據...")
get_metrics()
print("\n檢查服務健康狀態...")
check_health()
print("\n檢查 Item...")
get_item()
print(print("\n檢查 Product..."))
get_product()
