# services.py
from typing import Optional
from db import create_account, get_account_by_username, update_balance
from models import Account

class AccountExistsError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

def open_account(username: str, initial_balance: float = 0.0) -> Account:
    existing = get_account_by_username(username)
    if existing:
        raise AccountExistsError(f"Account with username '{username}' already exists.")
    acc_id = create_account(username, initial_balance)
    return Account(id=acc_id, username=username, balance=float(initial_balance))

def get_account(username: str) -> Optional[Account]:
    row = get_account_by_username(username)
    if not row:
        return None
    return Account(id=row["id"], username=row["username"], balance=float(row["balance"]))

def deposit(username: str, amount: float) -> Account:
    if amount <= 0:
        raise ValueError("Deposit amount must be positive.")
    acc = get_account(username)
    if not acc:
        raise ValueError("Account not found.")
    new_balance = acc.balance + amount
    update_balance(acc.id, new_balance)
    return get_account(username)

def withdraw(username: str, amount: float) -> Account:
    if amount <= 0:
        raise ValueError("Withdraw amount must be positive.")
    acc = get_account(username)
    if not acc:
        raise ValueError("Account not found.")
    if acc.balance < amount:
        raise InsufficientFundsError("Insufficient funds.")
    new_balance = acc.balance - amount
    update_balance(acc.id, new_balance)
    return get_account(username)
