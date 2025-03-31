import re
import sys
import uuid
from core.config import log
from imessage_reader import fetch_data
import os


class iMessages:
    def __init__(self) -> None:
        DB_PATH = os.getenv("DATA_DIRECTORY", "/Users/sumitsontakke/Documents/")
        log.info(f"DB_PATH: {DB_PATH}")
        # Check if the path exists
        if not os.path.exists(DB_PATH):
            log.error(f"Path does not exist: {DB_PATH}")
            sys.exit(1)
        # list of all files in the directory
        files = os.listdir(DB_PATH)
        log.info(f"Files in directory: {files}")
        
        # Create a FetchData instance
        fd = fetch_data.FetchData(DB_PATH + "chat.db")
        # Store messages in my_data
        # This is a list of tuples containing user id, message and service (iMessage or SMS).
        all_txnx = fd.get_messages()

        txn_stressors = [
            r"Sent Rs\.\d+\.\d+ from Kotak Bank AC X\d+",
            r"Sent Rs\.\d+\.\d+ from Kotak Bank AC X\d+ to \S+ on \d{2}-\d{2}-\d{2}",
            r"Thank you for using \S+ Credit Card No XX\d+ on \d{2}-\d{2}-\d{2} for INR \d+",
            r"Amt Sent Rs.\d+\nFrom HDFC Bank A/C *\d+\nTo \S+\nOn \d{2}-\d{2}\nRef \d+",
        ]

        parsed_msgs = list()
        for msg in all_txnx:
            parsed_msgs.append(msg) if [
                phrase
                for phrase in list(msg)
                if re.search(pattern=txn_stressors[0], string=str(phrase))
            ] else False

        self.msgs = parsed_msgs

    def get_messages(self):
        """
        Returns filtered imessages list with extracted fields like account_info, amount, to_id
        """
        filtered_msgs = self.msgs
        msgs = [self.extract_keys(msg) for msg in filtered_msgs]
        return msgs

    def extract_keys(
        self,
        msg,
        msg_keys=["sender", "text", "timestamp", "type", "receiver", "_number_"],
    ):
        # map keys and values to form data dictionary as per
        data = dict(zip(msg_keys, msg))

        data["id"] = str(uuid.uuid1())

        # extract amount and add to data dictionary
        amt_search = re.search(pattern=r"\d+", string=data.get("text", ""))
        currency_amt = (
            re.findall(
                pattern=r"Rs.\d+|INR\s*\d+|INR.\s*\d+", string=data.get("text", "")
            )
            if amt_search
            else False
        )
        amount_num = (
            [re.findall(pattern="\d+", string=cnum) for cnum in currency_amt]
            if currency_amt
            else False
        )
        if len(amount_num) >= 1:
            amt = (
                amount_num[-1]
                if amount_num and isinstance(amount_num[-1], list)
                else False
            )
            data["amount"] = amt

        # If txn about sending money using upi address, extract upi id and add to data dictionary
        to_id = re.findall(pattern=r"\S+@\S+", string=data.get("text", ""))
        if to_id:
            data["to_id"] = to_id

        # find account related information
        data["accounts_info"] = []
        acc_id = re.findall(pattern=r"\bX\d{2,6}\b", string=data.get("text", ""))
        if (
            acc_id
            and "bank ac"
            in data.get("text", "")[: data.get("text", "").index(acc_id[-1])].lower()
        ):
            data["accounts_info"].append(("bank_ac", acc_id))
            del acc_id
        acc_id = re.findall(pattern=r"\bXX\d{3,4}\b", string=data.get("text", ""))
        if (
            acc_id
            and "credit"
            in data.get("text", "")[: data.get("text", "").index(acc_id[-1])].lower()
            and "card"
            in data.get("text", "")[: data.get("text", "").index(acc_id[-1])].lower()
            and "credit card"
            in data.get("text", "")[: data.get("text", "").index(acc_id[-1])].lower()
        ):
            data["accounts_info"].append(("credit_card", acc_id))
            del acc_id

        return data

    def update_iPMessage(self):
        msgs = [self.extract_keys(msg) for msg in self.msgs]
        return msgs
