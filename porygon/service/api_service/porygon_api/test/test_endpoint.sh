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

curl -X GET "http://localhost:8080/api/v1/porygon/UserQuery/item/bcc4f2ff-1b65-4e28-b2bb-b0475fab73a2" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"

