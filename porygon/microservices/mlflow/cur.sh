


curl -X POST http://35.201.255.108/invocations \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"input":"Who is the biggest Pokemon?"}]}'

  curl -X POST http://35.201.255.108/v2/models/wikipedia/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "name": "input",
        "shape": [1],
        "datatype": "BYTES",
        "data": ["Who is the biggest Pokemon?"]
      }
    ]
  }'