import os
import sys
import re
import uuid
from core.config import log
from db.repository.grokPatterns import get_all_grok_patterns
from db.repository.txn_patterns import get_all_patterns
from imessage_reader import fetch_data


class iMessages:
    def __init__(self, db) -> None:
        """
        Initialize the iMessages class.
        - Sets up the database path from the environment variable or default path.
        - Loads Grok patterns and transaction patterns from the database.
        - Filters messages based on transaction patterns.
        """
        # Load Grok patterns from the database
        self.grok_patterns = get_all_grok_patterns(db)
        log.info(f"Grok patterns loaded: {self.grok_patterns}")

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

        # Load transaction patterns from the database
        txn_patterns = get_all_patterns(db)
        log.info(f"Transaction patterns loaded: {len(txn_patterns)}")
        if not txn_patterns:
            log.warning("No transaction patterns found in the database. Using default patterns.")
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

        Returns:
            list: A list of all raw iMessages.
        """
        log.info(f"Total raw messages count: {len(self.all_messages_raw)}")
        return self.all_messages_raw

    def get_messages(self):
        """
        Returns a list of filtered iMessages with extracted fields.
        - Extracts key information dynamically based on Grok patterns.

        Returns:
            list: A list of processed messages with extracted fields.
        """
        processed_msgs = [self.process_message(msg) for msg in self.msgs]
        log.info(f"Processed messages count: {len(processed_msgs)}")
        return processed_msgs

    def process_message(self, msg):
        """
        Processes a single message by extracting key entities dynamically.

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

        # Extract entities dynamically using Grok patterns
        extracted_fields = self.extract_key_fields(data.get("text", ""))
        data.update(extracted_fields)

        return data

    def extract_key_fields(self, text):
        """
        Dynamically extracts key fields from the message text using Grok patterns.

        Args:
            text (str): The message text.

        Returns:
            dict: A dictionary containing extracted fields and their values.
        """
        extracted_info = {}

        # Iterate over Grok patterns and apply them to the text
        for field, pattern in self.grok_patterns.items():
            matches = re.findall(pattern, text)  # Find all matches for the pattern
            if matches:
                # If the field already exists, append matches to the existing list
                if field in extracted_info:
                    extracted_info[field].extend(matches)
                else:
                    extracted_info[field] = matches

        return extracted_info

    def debug_message(self, msg):
        """
        Debug a single message by printing its raw and processed data.

        Args:
            msg (tuple): The message tuple containing raw data.

        Returns:
            None
        """
        log.info(f"Raw message: {msg}")
        processed_msg = self.process_message(msg)
        log.info(f"Processed message: {processed_msg}")
        return processed_msg