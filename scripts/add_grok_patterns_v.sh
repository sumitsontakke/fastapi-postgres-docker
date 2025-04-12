#!/bin/bash

# API Endpoint
API_URL="http://localhost/grokpatterns/"

# Declare patterns as an array of JSON payloads
patterns=(
  '{"field": "amount", "pattern": "Rs\\.\\d+\\.\\d+|INR \\d+", "description": "Extracts monetary amounts in formats like Rs.1234.56, INR 1234"}'
  '{"field": "account_info", "pattern": "\\S+ Bank AC X\\d+", "description": "Extracts account information such as X12345 from messages mentioning Bank accounts"}'
  '{"field": "credit_card_info", "pattern": "\\S+ Credit Card No XX\\d+", "description": "Extracts credit card references like XX1234"}'
  '{"field": "upi_id", "pattern": "\\S+@\\S+", "description": "Extracts UPI IDs in formats like user@bank"}'
  '{"field": "date", "pattern": "\\d{2}-\\d{2}-\\d{2}|\\d{2}/\\d{2}/\\d{4}", "description": "Extracts dates in formats like 12-12-23 or 12/12/2023"}'
  '{"field": "reference_number", "pattern": "Ref \\d+", "description": "Extracts reference numbers from messages like Ref 123456"}'
)

# Iterate over each pattern and send it to the API
for pattern in "${patterns[@]}"; do
  echo "Uploading pattern: $pattern"
  response=$(curl --silent --location "$API_URL" \
    --header 'Content-Type: application/json' \
    --data "$pattern")
  echo "Response: $response"
  echo "---"
done

echo "All patterns have been uploaded."
