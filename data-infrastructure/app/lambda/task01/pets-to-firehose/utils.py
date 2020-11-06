import json
from typing import List


def load_json(path) -> List[List[str]]:
    with open(path, mode="r", encoding="utf-8") as f:
        obj = json.load(f)
        return obj
