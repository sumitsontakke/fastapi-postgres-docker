#!/bin/bash

# Declare the array of patterns
declare -a PATTERNS=(
    "Sent Rs\\.\\d+\\.\\d+ from \\S+ Bank AC X\\d+"
    "Sent Rs\\.\\d+\\.\\d+ from \\S+ Bank AC X\\d+ to \\S+ on \\d{2}-\\d{2}-\\d{2}"
    "Thank you for using \\S+ Credit Card No XX\\d+ on \\d{2}-\\d{2}-\\d{2} for INR \\d+"
    "Amt Sent Rs\\.\\d+\\nFrom \\S+ Bank A/C \\*\\d+\\nTo \\S+\\nOn \\d{2}-\\d{2}\\nRef \\d+"
    "UPI Transaction of Rs\\.\\d+\\.\\d+ to \\S+@\\S+ completed"
    "UPI Payment of Rs\\.\\d+\\.\\d+ received from \\S+@\\S+"
    "Rs\\.\\d+\\.\\d+ debited from your account via UPI"
    "Cash withdrawal of Rs\\.\\d+\\.\\d+ from ATM \\S+ on \\d{2}-\\d{2}-\\d{2}"
    "ATM withdrawal of INR \\d+ on \\d{2}/\\d{2}/\\d{4}"
    "Payment of Rs\\.\\d+\\.\\d+ made to \\S+ via \\S+ Gateway"
    "Transaction of INR \\d+ completed via \\S+ Gateway"
    "Refund of Rs\\.\\d+\\.\\d+ has been credited to your account"
    "Refund of INR \\d+ processed for transaction ID \\S+"
    "EMI of Rs\\.\\d+\\.\\d+ debited from your account"
    "Loan repayment of INR \\d+ received on \\d{2}-\\d{2}-\\d{2}"
    "Your account has been credited with Rs\\.\\d+\\.\\d+"
    "Your account has been debited with Rs\\.\\d+\\.\\d+"
    "Transaction of Rs\\.\\d+\\.\\d+ failed due to insufficient balance"
)

# Define the API endpoint
API_ENDPOINT="http://localhost/txnpatterns/patterns"

# Loop through each pattern and make the POST request
for PATTERN in "${PATTERNS[@]}"; do
    # Prepare the JSON payload
    JSON_PAYLOAD=$(jq -n --arg pattern "$PATTERN" --arg description "Transaction pattern: $PATTERN" \
        '{pattern: $pattern, description: $description}')
    
    # Perform the POST API call
    curl -X POST "$API_ENDPOINT" \
         -H "Content-Type: application/json" \
         -d "$JSON_PAYLOAD"
done

echo "API calls completed for all patterns."
