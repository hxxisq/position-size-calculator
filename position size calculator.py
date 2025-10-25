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

def create_preset(account_name, account_balance, risk_percentage):
    """add a new account preset to the database"""
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (?,?,?)", (account_name, account_balance, risk_percentage))
    conn.commit()
    conn.close()

    print(f"\n{account_name} created successfully")

def get_all_presets():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("SELECT rowid, account_name, account_balance, risk_percentage FROM accounts")
    presets = c.fetchall()

    conn.close()

    return presets

def display_all_presets():
    """show all saved account preset"""
    presets = get_all_presets()

    if not presets:
        print("No presets saved")
        return

    for preset in presets:
        rowid = preset[0]
        name = preset[1]
        account_balance = preset[2]
        risk_percentage = preset[3]
        print(f"{rowid} || Name: {name} || Balance: {account_balance:,.2f} || Risk Percentage: {risk_percentage}%")

def delete_preset(rowid):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute("DELETE FROM accounts WHERE rowid = (?)", (rowid,))

    print("Preset deleted successfully")
    conn.commit()
    conn.close()

def show_menu():
    print("\nPosition size Calculator")
    print("Please select an option:")
    print("\n1. Calculate with preset")
    print("2. Create a new preset")
    print("3. View all presets")
    print("4. Delete a preset") # would later be under edit preset
    print("5. Exit")

    option = input("\nChoose an option: ").lower()
    return option

def calculate_lot_size (balance, risk_percent, stop_loss):
    risk_amount = balance * (risk_percent/100)
    pip_value = risk_amount / stop_loss
    mini_lots = pip_value / 1
    return{
        "risk_amount": risk_amount,
        "mini_lots": round(mini_lots, 2)
    }

def calculate_all_presets(stop_loss):
    presets = get_all_presets()

    if not presets:
        print("No presets saved, Create one first")
        return


    for p in presets:
        name = p[1]
        balance = p[2]
        risk_percent = p[3]

        result = calculate_lot_size(balance, risk_percent, stop_loss)

        print(f"\nAccount: {name} || Balance: {balance:,.2f} "
              f"|| Risk amount: ${result['risk_amount']:,.2f} "
              f"|| Position size: {result['mini_lots']:,.2f} mini lots")

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

def main():
    initialize_db()

    while True:
        option = show_menu()

        if option == "1": # calculate with preset
            while True:
                stop = get_number_input("\nEnter stop loss (pips):  ")
                calculate_all_presets(stop)

                try_again = input("\nWould you like to calculate again? (y/n): ").lower()
                if try_again == "y":
                    continue
                else:
                    input("Press enter to return to main menu...")
                    break

        elif option == "2": # create a new preset
            create_preset(
                account_name=input("\nEnter account name: "),
                account_balance=get_number_input("Enter account balance ($): "),
                risk_percentage=get_number_input("Enter risk percentage (%): "))
            input("\nPress enter to return to main menu...")

        elif option == "3": # view all presets
            print(" ")
            display_all_presets()
            input("\nPress enter to return to main menu...")

        elif option == "4": # delete a preset
            print(" ")
            display_all_presets()
            while True:
                try:
                    preset_id = int(input("\nEnter preset ID: "))

                    presets = get_all_presets()
                    valid_id = [p[0] for p in presets]

                    if preset_id not in valid_id:
                        print("Invalid preset ID!")
                    else:
                        delete_preset(preset_id)
                        input("\nPress enter to return to main menu...")
                        break
                except ValueError:
                    print("Invalid preset ID!")

        elif option == "5": # exit program
            print("\nThank you for using position size calculator")
            break
        else:
            print("\nInvalid input! please enter a number!")

if __name__ == "__main__":
    main()