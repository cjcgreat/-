# cli.py
import sys
from db import init_db, list_accounts
from services import open_account, deposit, withdraw, get_account, AccountExistsError, InsufficientFundsError

def print_help():
    print("Commands: init | create <username> <initial_balance> | deposit <username> <amount> | withdraw <username> <amount> | balance <username> | list | help | exit")

def main():
    init_db()
    print("Simple Bank CLI. Type 'help' for commands.")
    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()
        try:
            if cmd == "exit":
                break
            elif cmd == "help":
                print_help()
            elif cmd == "init":
                init_db()
                print("DB initialized.")
            elif cmd == "create" and len(parts) >= 2:
                username = parts[1]
                initial = float(parts[2]) if len(parts) > 2 else 0.0
                try:
                    acc = open_account(username, initial)
                except AccountExistsError as e:
                    print("Error:", e)
                else:
                    print("Created:", acc)
            elif cmd == "deposit" and len(parts) == 3:
                username, amount = parts[1], float(parts[2])
                acc = deposit(username, amount)
                print("New balance:", acc.balance)
            elif cmd == "withdraw" and len(parts) == 3:
                username, amount = parts[1], float(parts[2])
                try:
                    acc = withdraw(username, amount)
                    print("New balance:", acc.balance)
                except InsufficientFundsError as e:
                    print("Error:", e)
            elif cmd == "balance" and len(parts) == 2:
                acc = get_account(parts[1])
                if not acc:
                    print("Account not found.")
                else:
                    print(f"{acc.username}: {acc.balance:.2f}")
            elif cmd == "list":
                rows = list_accounts()
                for r in rows:
                    print(f"{r['id']}\t{r['username']}\t{r['balance']:.2f}")
            else:
                print("Unknown command or wrong args. Type 'help'.")
        except Exception as e:
            print("Unhandled error:", e)

if __name__ == "__main__":
    main()
