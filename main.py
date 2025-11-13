# main.py
from db import init_db
from services import open_account, deposit, withdraw, get_account, AccountExistsError, InsufficientFundsError

def smoke_test():
    init_db()
    try:
        open_account("alice", 100.0)
    except AccountExistsError:
        pass
    print("Alice initial:", get_account("alice").balance)
    deposit("alice", 50.0)
    print("After deposit:", get_account("alice").balance)
    try:
        withdraw("alice", 200.0)
    except InsufficientFundsError:
        print("Caught insufficient funds as expected.")
    withdraw("alice", 50.0)
    print("After withdraw:", get_account("alice").balance)

if __name__ == "__main__":
    smoke_test()
