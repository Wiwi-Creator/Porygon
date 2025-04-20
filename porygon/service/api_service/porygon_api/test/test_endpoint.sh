curl -X GET \
  http://localhost:8080/health \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"

  curl -X POST \
  http://localhost:8080/api/v1/porygon/AIservice/wikipedia_agent/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{"query": "Who is the biggest Pokemon?"}'

  curl -X POST "http://localhost:8080/api/v1/porygon/item" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{
    "name": "測試產品",
    "description": "這是一個測試產品",
    "price": 199.99,
    "quantity": 10,
    "category": "電子產品",
    "tags": ["測試", "新品"],
    "properties": {
      "color": "黑色",
      "weight": "200g"
    }
  }'

curl -X POST "http://localhost:8080/api/v1/porygon/UserQuery/item/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{
    "name": "Firestore測試產品",
    "description": "這是存儲在Firestore的測試產品",
    "price": 299.99,
    "quantity": 5,
    "category": "測試類別",
    "tags": ["firestore", "測試"],
    "properties": {
      "source": "API測試"
    },
    "collection": "products"
  }'
