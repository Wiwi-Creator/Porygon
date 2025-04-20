curl -X GET \
  http://localhost:8080/health \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"

  curl -X POST \
  http://localhost:8080/api/v1/porygon/AIservice/wikipedia_agent/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{"query": "Who is the biggest Pokemon?"}'

# Test on premise
curl -X GET "http://localhost:8080/api/v1/porygon/UserQuery/resource/GetItems/bcc4f2ff-1b65-4e28-b2bb-b0475fab73a2" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"


curl -X GET "http://localhost:8080/api/v1/porygon/UserQuery/resource/GetProducts/Product/A123" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"


curl -X POST "http://localhost:8080/api/v1/porygon/AIservice/wikipedia_agent"/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{"query": "Who is the biggest Pokemon?"}'
