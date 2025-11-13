# models.py
from dataclasses import dataclass

@dataclass
class Account:
    id: int
    username: str
    balance: float
