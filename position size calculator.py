import sqlite3


def initialize_db():
    # connects to database
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    # create table
    c.execute("""CREATE TABLE IF NOT EXISTS accounts(
            account_name text,
            account_balance real,
            risk_percentage real
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized")

def create_accounts(account_name, account_balance, risk_percentage):
    """add a new account preset to the database"""
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (?,?,?)", (account_name, account_balance, risk_percentage))
    conn.commit()
    conn.close()

    print(f"{account_name} created successfully")

def get_all_accounts():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("SELECT rowid, account_name, account_balance, risk_percentage FROM accounts")
    accounts = c.fetchall()

    conn.close()

    return accounts

def display_all_accounts():
    """show all saved accounts"""
    accounts = get_all_accounts()

    if not accounts:
        print("No accounts saved")
        return

    for item in accounts:
        rowid = item[0]
        name = item[1]
        account_balance = item[2]
        risk_percentage = item[3]
        print(f"{rowid} || Name: {name} || Balance: {account_balance:,.2f} || Risk Percentage: {risk_percentage}%")

def delete_accounts(rowid):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute("DELETE FROM accounts WHERE rowid = (?)", (rowid,))

    conn.commit()
    conn.close()

def calculate_lot_size (balance, risk_percent, stop_loss):
    risk_amount = balance * (risk_percent/100)
    pip_value = risk_amount / stop_loss
    mini_lots = pip_value / 1
    return{
        "risk_amount": risk_amount,
        "mini_lots": round(mini_lots, 2)
    }

def get_number_input(user_input):
    while True:
        try:
            value = float(input(user_input))
            if value <= 0:
                print("Enter a positive number!")
                continue #this restarts the loop
            return value
        except ValueError:
            print("Invalid input! please enter a number!")

# def main():
#     print('POSITION SIZE CALCULATOR')
#
#     while True:
#         #get user input
#         account_balance = get_number_input("\nAccount balance($): ")
#         risk_percent = get_number_input("Risk percent(%): ")
#         stop_loss = get_number_input("Stop loss(pips): ")
#
#         #calculate lots size
#         result = calculate_lot_size(account_balance, risk_percent, stop_loss)
#
#         #display result
#         print(f"Risk: ${result['risk_amount']}\nMini lot: {result['mini_lots']}")
#
#         #ask if user wants to calculate again
#         repeat = input("\nWant to calculate again? (y/n) ").lower()
#         if repeat != "y":
#             break
#
# if __name__ == '__main__':
#     main()

def main():
    initialize_db()

if __name__ == "__main__":
    main()
