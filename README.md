Here’s a comprehensive project documentation that includes all the changes we’ve made so far, along with explanations and usage instructions. This documentation is structured to cater to the developer community and is suitable for a GitHub repository.

---

# **iMessages Transaction Parser**

## **Overview**
The `iMessages Transaction Parser` is a Python-based project designed to extract meaningful financial information from iMessage text messages. It dynamically adapts to new message formats by leveraging Grok patterns stored in a database. This project is ideal for personal use to compute bank balances, credit card spendings, and other financial transactions. It also supports community contributions for enhancements and bug fixes.

---

## **Features**
1. **Dynamic Grok Pattern Loading**:
   - Grok patterns are stored in a database and dynamically loaded at runtime, allowing the system to adapt to new message formats without code changes.

2. **Field Extraction**:
   - Extracts key fields such as `amount`, `account`, `upi_id`, `timestamp`, and `merchant` from text messages.

3. **Handles Multiple Matches**:
   - Supports multiple patterns for a single field (e.g., `amount`) and aggregates all matches into a list.

4. **Scalable and Maintainable**:
   - Centralized pattern management in the database ensures scalability and ease of maintenance.

5. **Developer-Friendly**:
   - Designed for the developer community to use, enhance, and contribute.

---

## **Project Structure**
```
fastapi-postgres-docker/
├── apis/
│   ├── base.py                # API routing
│   ├── v1/
│   │   ├── route_txnPatterns.py  # API endpoints for managing Grok patterns
├── business/
│   ├── definitions/
│   │   ├── iMessages.py       # Core logic for parsing iMessages
├── db/
│   ├── models/
│   │   ├── grokPatterns.py    # Database model for Grok patterns
│   │   ├── txnPatterns.py     # Database model for transaction patterns
│   ├── repository/
│   │   ├── grokPatterns.py    # Repository for managing Grok patterns
│   │   ├── txnPatterns.py     # Repository for managing transaction patterns
│   ├── session.py             # Database session management
├── scripts/
│   ├── load_txn_patterns.sh   # Shell script to load transaction patterns into the database
├── core/
│   ├── config.py              # Logging and configuration
├── README.md                  # Project documentation
```

---

## **Installation**

### **Prerequisites**
- Python 3.9+
- PostgreSQL
- Docker (optional, for containerized deployment)

### **Steps**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/imessages-transaction-parser.git
   cd imessages-transaction-parser
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Create a PostgreSQL database.
   - Update the database connection string in config.py.

5. **Run Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the Application**:
   ```bash
   uvicorn main:app --reload
   ```

---

## **Usage**

### **1. Add Grok Patterns**
Use the `/grokpatterns` API endpoint to add Grok patterns for extracting fields.

#### **Example Request**
```bash
curl --location 'http://localhost:8000/grokpatterns' \
--header 'Content-Type: application/json' \
--data '{
    "field": "amount",
    "pattern": "(?:Rs\\.|INR)\\s?(\\d{1,3}(?:,\\d{3})*(?:\\.\\d{1,2})?)",
    "description": "Extracts amounts in formats like Rs.1234.56 or INR 1,234.56"
}'
```

### **2. Load Transaction Patterns**
Run the `load_txn_patterns.sh` script to load predefined transaction patterns into the database.

```bash
./scripts/load_txn_patterns.sh
```

### **3. Parse iMessages**
Use the `iMessages` class to parse iMessages and extract key fields.

#### **Example Code**
```python
from db.session import get_db
from business.definitions.iMessages import iMessages

# Get the database session
db = next(get_db())

# Initialize iMessages
imessages = iMessages(db)

# Get processed messages
processed_messages = imessages.get_messages()
print(processed_messages)
```

---

## **How It Works**

### **1. Dynamic Grok Pattern Loading**
- Grok patterns are stored in the `GrokPattern` table.
- At runtime, the `iMessages` class fetches these patterns and applies them to extract fields dynamically.

### **2. Field Extraction**
- The `extract_key_fields` method uses regex patterns to extract fields like `amount`, `account`, `upi_id`, etc.
- Multiple matches for a single field are stored in a list.

### **3. Transaction Filtering**
- Messages are filtered using transaction patterns stored in the `txnPatterns` table.

---

## **Contributing**

### **How to Contribute**
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.

### **Contribution Guidelines**
- Follow PEP 8 for Python code.
- Write clear and concise commit messages.
- Add tests for new features or bug fixes.

---

## **Future Enhancements**
1. **Support for Additional Message Formats**:
   - Add more Grok patterns to handle diverse message formats.

2. **Improved Error Handling**:
   - Enhance error handling for edge cases.

3. **Web Interface**:
   - Build a web interface for managing patterns and viewing parsed messages.

4. **Integration with Financial Tools**:
   - Export parsed data to financial tools like Excel or budgeting apps.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

## **Acknowledgments**
- Inspired by the need for better personal finance tracking tools.
- Thanks to the developer community for their contributions and feedback.
