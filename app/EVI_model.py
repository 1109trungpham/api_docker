

import json
from pydantic_model import Model

with open("muhammed15.json", "r", encoding="utf-8") as file:
    raw_data = json.load(file)

try:
    validated_data = Model(**raw_data)
    print(validated_data)
except Exception as e:
    print("Validation Error:", e)

    