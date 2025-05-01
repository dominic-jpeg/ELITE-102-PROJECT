import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='skibiditoilet123!',
    database='banking_system'
) 
cursor = conn.cursor()

def login():
    acc = input("Enter Account Number: ")
    pin = input("Enter PIN: ")
    cursor.execute("SELECT * FROM accounts WHERE account_number = %s AND pin = %s", (acc, pin))
    user = cursor.fetchone()
    if user:
        print("\nLogin successful!\n")
        usermenu(user[0])
    else:
        print("\nInvalid account number or PIN!\n")

def usermenu(accountnumber):
    while True:
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")
        choice = input("Choose an option: ")
        if choice == '1':
            checkbalance(accountnumber)
        elif choice == '2':
            deposit(accountnumber)
        elif choice == '3':
            withdraw(accountnumber)
        elif choice == '4':
            break
        else:
            print("Invalid option!")

def checkbalance(accountnumber):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (accountnumber,))
    balance = cursor.fetchone()[0]
    print(f"\nYour current balance is: ${balance}\n")

def deposit(accountnumber):
    amount = float(input("Enter amount to deposit: "))
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, accountnumber))
    conn.commit()
    print("\nDeposit successful!\n")

def withdraw(accountnumber):
    amount = float(input("Enter amount to withdraw: "))
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (accountnumber,))
    balance = cursor.fetchone()[0]
    if amount > balance:
        print("\nInsufficient balance!\n")
    else:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (amount, accountnumber))
        conn.commit()
        print("\nWithdrawal successful!\n")

def createaccount():
    acc = input("Enter new account number: ")
    pin = input("Set a 4-digit PIN: ")
    name = input("Enter your name: ")
    cursor.execute("INSERT INTO accounts (account_number, pin, name) VALUES (%s, %s, %s)", (acc, pin, name))
    conn.commit()
    print("\nAccount created successfully!\n")

def closeaccount():
    acc = input("Enter account number to close: ")
    cursor.execute("DELETE FROM accounts WHERE account_number = %s", (acc,))
    conn.commit()
    print("\nAccount closed successfully!\n")

def modifyaccount():
    acc = input("Enter account number to modify: ")
    print("1. Change Name")
    print("2. Change PIN")
    choice = input("Choose an option: ")
    if choice == '1':
        newname = input("Enter new name: ")
        cursor.execute("UPDATE accounts SET name = %s WHERE account_number = %s", (newname, acc))
    elif choice == '2':
        newpin = input("Enter new 4-digit PIN: ")
        cursor.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (newpin, acc))
    else:
        print("Invalid choice!")
        return
    conn.commit()
    print("\nAccount updated successfully!\n")

while True:
    print("\nWelcome to the Bank")
    print("1. Login")
    print("2. Create Account")
    print("3. Close Account")
    print("4. Modify Account")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        login()
    elif choice == '2':
        createaccount()
    elif choice == '3':
        closeaccount()
    elif choice == '4':
        modifyaccount()
    elif choice == '5':
        break
    else:
        print("Invalid option!")