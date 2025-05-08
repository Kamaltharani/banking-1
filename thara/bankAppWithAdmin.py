from tabulate import tabulate
from datetime import datetime
import json

# Global variables
accounts = {}
next_account_number = 1001  # Auto-generated starting account number
admin_account = {"username": "admin", "password": "admin123"}  # set password for default admin account

# Load accounts and admin data from file if exists
def load_accounts():
    global accounts, next_account_number, admin_account
    try:
        with open("accounts_data.json", "r") as f:
            data = json.load(f)
            accounts = data.get("accounts", {})
            next_account_number = data.get("next_account_number", 1001)
            admin_account = data.get("admin_account", admin_account)
    except FileNotFoundError:
        pass

def save_accounts():
    with open("accounts_data.json", "w") as f:
        data = {
            "accounts": accounts,
            "next_account_number": next_account_number,
            "admin_account": admin_account
        }
        json.dump(data, f)

def create_account():
    global next_account_number
    name = input("Enter account holder's name: ")
    password = input("Set a password for your account: ")

    while True:
        try:
            initial_balance = float(input("Enter initial deposit amount: "))
            if initial_balance < 0:
                print("Initial balance cannot be negative. Try again.")
            else:
                break
        except ValueError:
            print("Please enter a valid amount.")

    account_number = next_account_number
    next_account_number += 1

    accounts[str(account_number)] = {
        'name': name,
        'password': password,
        'balance': initial_balance,
        'transactions': [("Initial deposit", initial_balance)]
    }

    save_accounts()
    print(f"Account created successfully! Your account number is {account_number}.")

def authenticate(account_number):
    password = input("Enter password: ")
    if accounts.get(str(account_number)) and accounts[str(account_number)]['password'] == password:
        return True
    else:
        print("Authentication failed.")
        return False

def deposit_money():
    acc_num = input("Enter your account number: ")
    password = input("Enter your account password: ")
    if acc_num in accounts and accounts[acc_num]['password'] == password:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        description = input("Enter a description for this deposit: ")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[acc_num]['balance'] += amount
        accounts[acc_num]['transactions'].append(("Deposit", amount, timestamp, description))
        print("Deposit successful.")
    else:
        print("Invalid account number or password.")

def withdraw_money():
    acc_num = input("Enter your account number: ")
    password = input("Enter your account password: ")
    if acc_num in accounts and accounts[acc_num]['password'] == password:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > accounts[acc_num]['balance']:
            print("Insufficient funds.")
            return
        description = input("Enter a description for this withdrawal: ")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[acc_num]['balance'] -= amount
        accounts[acc_num]['transactions'].append(("Withdrawal", amount, timestamp, description))
        print("Withdrawal successful.")
    else:
        print("Invalid account number or password.")

def check_balance():
    try:
        account_number = int(input("Enter account number: "))
        if str(account_number) in accounts:
            if authenticate(account_number):
                balance = accounts[str(account_number)]['balance']
                print(f"Current balance for account {account_number} is {balance:.2f}")
        else:
            print("Account not found.")
    except ValueError:
        print("Invalid input. Please enter a valid account number.")

def transaction_history():
    acc_num = input("Enter your account number: ")
    password = input("Enter your account password: ")
    if acc_num in accounts and accounts[acc_num]['password'] == password:
        show_transaction_history(acc_num)
    else:
        print("Invalid account number or password.")

def show_transaction_history(acc_num):
    account = accounts[acc_num]
    balance = account['balance']
    print(f"\nCurrent balance: {balance}")

    if not account['transactions']:
        print("No transactions yet.")
        return

    headers = ["Type", "Amount", "Timestamp", "Description"]
    table = []

    for txn in account['transactions']:
        if len(txn) == 4:
            txn_type, amount, timestamp, description = txn
            table.append([txn_type, amount, timestamp, description])
        else:
            table.append(list(txn) + ["", ""])

    print(f"\nTransaction History for Account {acc_num}:")
    print(tabulate(table, headers, tablefmt="grid"))

def transfer_money():
    from_acc = input("Enter your account number: ")
    password = input("Enter your account password: ")
    if from_acc in accounts and accounts[from_acc]['password'] == password:
        to_acc = input("Enter recipient account number: ")
        if to_acc in accounts:
            amount = float(input("Enter amount to transfer: "))
            if amount > 0:
                if accounts[from_acc]['balance'] >= amount:
                    description = input("Enter a description for this transfer: ")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    accounts[from_acc]['balance'] -= amount
                    accounts[to_acc]['balance'] += amount
                    accounts[from_acc]['transactions'].append(("Transfer Sent", amount, timestamp, description))
                    accounts[to_acc]['transactions'].append(("Transfer Received", amount, timestamp, description))
                    print("Transfer successful.")
                else:
                    print("Insufficient balance for transfer.")
            else:
                print("Transfer amount must be positive.")
        else:
            print("Recipient account does not exist.")
    else:
        print("Invalid account number or password.")

def calculate_interest():
    try:
        account_number = int(input("Enter account number: "))
        if str(account_number) in accounts:
            if authenticate(account_number):
                rate = float(input("Enter annual interest rate (in %): "))
                years = float(input("Enter number of years: "))
                principal = accounts[str(account_number)]['balance']
                interest = (principal * rate * years) / 100
                accounts[str(account_number)]['balance'] += interest
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                accounts[str(account_number)]['transactions'].append(("Interest Added", interest, timestamp, "Interest"))
                save_accounts()
                print(f"Interest of {interest:.2f} added successfully!")
        else:
            print("Account not found.")
    except ValueError:
        print("Invalid input. Please enter numeric values.")

# === ADMIN FUNCTIONALITIES ===

def admin_login():
    print("\n--- Admin Login ---")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == admin_account['username'] and password == admin_account['password']:
        print("Admin login successful.")
        admin_menu()
    else:
        print("Invalid admin credentials.")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View All User Balances")
        print("2. View User Transaction History")
        print("3. Change Admin Password")
        print("4. Exit Admin Menu")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_all_balances()
        elif choice == '2':
            view_user_transaction()
        elif choice == '3':
            change_admin_password()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def view_all_balances():
    if not accounts:
        print("No user accounts found.")
        return
    headers = ["Account Number", "Name", "Balance"]
    rows = []
    for acc_num, details in accounts.items():
        rows.append([acc_num, details['name'], details['balance']])
    print("\nAll User Account Balances:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def view_user_transaction():
    acc_num = input("Enter user account number to view history: ")
    if acc_num in accounts:
        show_transaction_history(acc_num)
    else:
        print("Account not found.")

def change_admin_password():
    old_password = input("Enter current admin password: ")
    if old_password == admin_account['password']:
        new_password = input("Enter new admin password: ")
        admin_account['password'] = new_password
        save_accounts()
        print("Admin password changed successfully.")
    else:
        print("Incorrect current password.")

# === MAIN MENU ===

def main_menu():
    load_accounts()
    while True:
        print("\n=== Mini Banking Application ===")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Transfer Money (Bonus)")
        print("7. Calculate Interest (Bonus)")
        print("8. Exit")
        print("9. Admin Login")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            transaction_history()
        elif choice == '6':
            transfer_money()
        elif choice == '7':
            calculate_interest()
        elif choice == '8':
            print("Thank you for using Mini Banking Application. Goodbye!")
            break
        elif choice == '9':
            admin_login()
        else:
            print("Invalid choice. Please select from 1 to 9.")

if __name__ == "__main__":
    main_menu()
