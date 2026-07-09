import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config"


def load_json(filename: str) -> Any:
    path = CONFIG_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
