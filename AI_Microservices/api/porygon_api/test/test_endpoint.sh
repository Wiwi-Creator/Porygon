curl -X GET \
  http://localhost:8080/health \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"

curl -X GET \
  http://localhost:8080/metric \
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

https://porygon-api-931091704211.asia-east1.run.app/docs


# test on cloud run 
# TO-DO ! Need VPC or interal IP
curl -X GET "https://porygon-api-931091704211.asia-east1.run.app/api/v1/porygon/UserQuery/resource/GetItems/bcc4f2ff-1b65-4e28-b2bb-b0475fab73a2" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"

curl -X GET "https://porygon-api-931091704211.asia-east1.run.app/api/v1/porygon/UserQuery/resource/GetProducts/Product/A123" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key"


# cquery from MLflow model
# Need VPC 
curl -X POST "https://porygon-api-931091704211.asia-east1.run.app/api/v1/porygon/AIservice/wikipedia_agent" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: admin_key" \
    -d '{"query": "Who is the biggest Pokemon?"}'
  

curl -X POST "https://porygon-api-931091704211.asia-east1.run.app/api/v1/porygon/AIservice/wikipedia_agent" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key" \
  -d '{"query": "Who is the biggest Pokemon?"}'

curl "https://porygon-api-931091704211.asia-east1.run.app/metric?date=2025-04-20" \
  -H "X-API-Key: admin_key"


curl "https://porygon-api-931091704211.asia-east1.run.app/health" \
  -H "X-API-Key: admin_key"