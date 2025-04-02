#!/bin/bash

# API Endpoint
API_URL="http://localhost/grokpatterns/"

# Declare patterns as an array of JSON payloads
patterns=(
  '{"field": "amount", "pattern": "(?:Rs\\\\.|INR)\\\\s?(\\\\d{1,3}(?:,\\\\d{3})*(?:\\\\.\\\\d{1,2})?)", "description": "Extracts amounts in formats like Rs.1234.56 or INR 1,234.56"}'
  '{"field": "account_info", "pattern": "\\\\b(?:A/C|Account)\\\\s?(\\\\d{9,18})\\\\b", "description": "Extracts account numbers from phrases like A/C 123456789012345678 or Account 123456789012"}'
  '{"field": "currency", "pattern": "\\\\b(?:Rs\\\\.|INR|USD|EUR)\\\\b", "description": "Extracts currency codes such as Rs., INR, USD, or EUR"}'
  '{"field": "upi_id", "pattern": "\\\\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+)\\\\b", "description": "Extracts UPI IDs in formats like user@bank or user123@xyzbank"}'
  '{"field": "account_info_extra", "pattern": "\\\\bX\\\\d{2,6}\\\\b", "description": "Extracts account identifiers like X123 or X123456"}'
  '{"field": "credit_card_transaction", "pattern": "\\\\b(?:Credit Card|Card ending in \\\\d{4})\\\\b", "description": "Identifies transactions involving credit cards with patterns like Credit Card or Card ending in XXXX"}'
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
