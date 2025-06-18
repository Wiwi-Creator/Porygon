curl -X GET \
  http://localhost:8080/health \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"

curl -X POST \
  http://localhost:8080/api/v1/porygon/AIservice/wikipedia_agent/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{"query": "Who is the biggest Pokemon?"}'