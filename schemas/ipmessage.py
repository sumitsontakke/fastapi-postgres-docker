from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, root_validator


class createIPMessage(BaseModel):
    sender: str
    text: str
    timestamp: datetime  # Changed to datetime for proper timestamp handling
    type: str
    receiver: str
    _number_: str
    amount: list[int] # In case message get parsed for multiple amounts, user shall fix this
    accounts_info: Union[str, List[tuple]]  # Supports both string and list formats
    to_id: Optional[Union[str, List[str]]] = ""

    @root_validator(pre=True)
    def validate_fields(cls, values):
        """
        Custom validation logic for fields.
        - Ensures `amount` is a positive integer.
        - Converts `accounts_info` to a string if it's a list or dict.
        """
        amount = values.get("amount", [])
        # Validate `amount` list, that every element value shall be positive number. If the element is string check if value of string is number then accept the value. If not, remove non integer values from list
        if "amount" in values:
            amount = values["amount"]
            if isinstance(amount, list):
                values["amount"] = [int(a) for a in amount if isinstance(a, (int, str)) and str(a).isdigit()]
            else:
                raise ValueError("Amount must be a list of positive integers or strings that can be converted to integers.")
        else:
            values["amount"] = [0]



        # Serialize `accounts_info` if it's a list or dict
        accounts_info = values.get("accounts_info")
        try:
            accounts_info = eval(accounts_info)
        except (SyntaxError, NameError):
            pass
        if isinstance(accounts_info, (list, dict)):
            import json
            values["accounts_info"] = json.dumps(accounts_info)

        return values