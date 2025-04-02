import re
import sys
import uuid
import os
from core.config import log
from imessage_reader import fetch_data
from db.repository.txn_patterns import get_all_patterns
from db.session import get_db

class iMessages:
    def __init__(self, db) -> None:
        """
        Initialize the iMessages class.
        - Sets up the database path from the environment variable or default path.
        - Validates the existence of the database path.
        - Loads messages from the iMessage database.
        - Filters messages based on predefined transaction patterns.
        """
        # Get the database path from the environment variable or use the default path
        DB_PATH = os.getenv("DATA_DIRECTORY", "/Users/sumitsontakke/Documents/mbt_data/")
        log.info(f"DB_PATH: {DB_PATH}")

        # Check if the database path exists
        if not os.path.exists(DB_PATH):
            log.error(f"Path does not exist: {DB_PATH}")
            sys.exit(1)

        # List all files in the directory for debugging purposes
        files = os.listdir(DB_PATH)
        log.info(f"Files in directory: {files}")

        # Initialize FetchData with the iMessage database file
        fd = fetch_data.FetchData(DB_PATH + "chat.db")

        # Fetch all messages from the database
        all_messages = fd.get_messages()

        # Define patterns to identify transaction-related messages
        txn_patterns = get_all_patterns(db)
        log.info(f"Transaction patterns loaded: #{len(txn_patterns)}")
        if not txn_patterns:
            txn_patterns = [
                r"Sent Rs\.\d+\.\d+ from Kotak Bank AC X\d+",
                r"Sent Rs\.\d+\.\d+ from Kotak Bank AC X\d+ to \S+ on \d{2}-\d{2}-\d{2}",
                r"Thank you for using \S+ Credit Card No XX\d+ on \d{2}-\d{2}-\d{2} for INR \d+",
                r"Amt Sent Rs.\d+\nFrom HDFC Bank A/C *\d+\nTo \S+\nOn \d{2}-\d{2}\nRef \d+",
            ]

        # Filter messages that match any of the transaction patterns
        filtered_messages = [
            msg
            for msg in all_messages
            if any(re.search(pattern, str(msg)) for pattern in txn_patterns)
        ]

        # Store the filtered messages for further processing
        self.msgs = filtered_messages
        self.all_messages_raw = all_messages

    def get_all_raw_messages(self):
        """
        Returns all raw iMessages without filtering.
        - Useful for debugging or when no filtering is needed.
        """
        # Return all messages without filtering
        log.info(f"Total messages count: {len(self.msgs)}")
        return self.all_messages_raw

    def get_messages(self):
        """
        Returns a list of filtered iMessages with extracted fields.
        - Extracts key information such as sender, text, timestamp, type, receiver, and more.
        """
        # Extract key information from each filtered message
        processed_msgs = [self.process_message(msg) for msg in self.msgs]
        log.info(f"Processed messages count: {len(processed_msgs)}")
        return processed_msgs

    def process_message(self, msg):
        """
        Processes a single message by extracting key entities.
        - Combines all entity extraction functions to process the message.

        Args:
            msg (tuple): The message tuple containing raw data.

        Returns:
            dict: A dictionary containing the extracted message data.
        """
        # Map predefined keys to message fields
        msg_keys = ["sender", "text", "timestamp", "type", "receiver", "_number_"]
        data = dict(zip(msg_keys, msg))

        # Generate a unique ID for the message
        data["id"] = str(uuid.uuid4())

        # Extract entities from the message
        data["amount"] = self.extract_amount(data.get("text", ""))
        data["to_id"] = self.extract_upi_id(data.get("text", ""))
        data["accounts_info"] = self.extract_account_info(data.get("text", ""))

        return data

    def extract_amount(self, text):
        """
        Extracts transaction amounts from the message text.

        Args:
            text (str): The message text.

        Returns:
            list: A list of extracted amounts.
        """
        # Define patterns to identify amounts
        amount_patterns = [
            r"Rs\.\d+",
            r"INR\s*\d+",
            r"INR.\s*\d+",
        ]

        # Extract amounts using the patterns
        currency_amt = [
            match.group() for pattern in amount_patterns for match in re.finditer(pattern, text)
        ]

        # Extract numeric values from the matched amounts
        amount_num = [int(num) for amt in currency_amt for num in re.findall(r"\d+", amt)]
        return amount_num if amount_num else None

    def extract_upi_id(self, text):
        """
        Extracts UPI IDs from the message text.

        Args:
            text (str): The message text.

        Returns:
            list: A list of extracted UPI IDs.
        """
        # Define pattern to identify UPI IDs
        upi_pattern = r"\S+@\S+"

        # Extract UPI IDs using the pattern
        return re.findall(upi_pattern, text)

    def extract_account_info(self, text):
        """
        Extracts account-related information from the message text.

        Args:
            text (str): The message text.

        Returns:
            list: A list of tuples containing account information.
        """
        accounts_info = []

        # Define patterns to identify bank account numbers
        bank_account_patterns = [
            r"\bX\d{2,6}\b",  # Bank account numbers (e.g., X1234)
        ]

        # Extract bank account numbers
        for pattern in bank_account_patterns:
            acc_id = re.findall(pattern, text)
            if acc_id and "bank ac" in text[: text.index(acc_id[-1])].lower():
                accounts_info.append(("bank_ac", acc_id))

        # Define patterns to identify credit card numbers
        credit_card_patterns = [
            r"\bXX\d{3,4}\b",  # Credit card numbers (e.g., XX1234)
        ]

        # Extract credit card numbers
        for pattern in credit_card_patterns:
            acc_id = re.findall(pattern, text)
            if (
                acc_id
                and "credit" in text[: text.index(acc_id[-1])].lower()
                and "card" in text[: text.index(acc_id[-1])].lower()
                and "credit card" in text[: text.index(acc_id[-1])].lower()
            ):
                accounts_info.append(("credit_card", acc_id))

        return accounts_info