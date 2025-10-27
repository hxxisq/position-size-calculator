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
    print("===Position size Calculator===".upper())
    print("Please select an option:")
    print("\n1. Calculate without preset (Quick)")
    print("2. Calculate with preset")
    print("3. Create a new preset")
    print("4. View all presets")
    print("5. Update a preset")
    print("6. Delete a preset")
    print("7. Exit")

    option = input("\nChoose an option: ").lower()
    return option

def calculate_lot_size (balance, risk_percentage, stop_loss):
    risk_amount = balance * (risk_percentage / 100)
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

def get_optional_number_input(user_input):
    while True:
        try:
            value = input(user_input).strip()
            if not value:
                return None

            number = float(value)

            if number <= 0:
                print("Enter a positive number!")
                continue

            return number

        except ValueError:
            print("Invalid input! please enter a number!")

def update_preset(rowid, new_name=None, new_balance=None, new_risk=None):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    fields = []
    values = []

    if new_name is not None:
        fields.append("account_name = ?")
        values.append(new_name)
    if new_balance is not None:
        fields.append("account_balance = ?")
        values.append(new_balance)
    if new_risk is not None:
        fields.append("risk_percentage = ?")
        values.append(new_risk)

    if not fields:
        print("Nothing to update")
        conn.close()
        return

    query = f"UPDATE accounts SET {', '.join(fields)} WHERE rowid = ?"
    values.append(rowid)

    c.execute(query, values)

    conn.commit()
    conn.close()

    print(f"\nPreset ID {rowid} updated successfully")

def main():
    initialize_db()

    while True:
        option = show_menu()

        if option == "1": # calculate without preset
            while True:
                result = calculate_lot_size(
                    balance= get_number_input("\nEnter account balance ($): "),
                    risk_percentage=get_number_input("Enter risk percentage (%): "),
                    stop_loss=get_number_input("Enter stop loss (pips): ")
                )

                print(f"\nRisk amount: ${result['risk_amount']:,.2f}")
                print(f"Position size: {result['mini_lots']:,.2f} mini lots")

                try_again = input("\nWould you like to calculate again? (y/n): ").lower()
                if try_again == "y":
                    continue
                else:
                    input("\nPress enter to return to main menu...")
                    break

        elif option == "2": # calculate with preset
            presets = get_all_presets()
            if not presets:
                input("\nNo presets Saved\n\nPress Enter to return to the main menu...")
                continue

            while True:
                stop = get_number_input("\nEnter stop loss (pips):  ")
                calculate_all_presets(stop)

                try_again = input("\nWould you like to calculate again? (y/n): ").lower()
                if try_again == "y":
                    continue
                else:
                    input("Press enter to return to main menu...")
                    break

        elif option == "3": # create a new preset
            create_preset(
                account_name=input("\nEnter account name: "),
                account_balance=get_number_input("Enter account balance ($): "),
                risk_percentage=get_number_input("Enter risk percentage (%): "))
            input("\nPress enter to return to main menu...")

        elif option == "4": # view all presets
            print(" ")
            display_all_presets()
            input("\nPress enter to return to main menu...")

        elif option == "5": # update a preset
            print(" ")
            display_all_presets()

            presets = get_all_presets()
            if not presets:
                input("\nPress Enter to return to the main menu...")
                continue

            try:
                preset_id = int(input("\nEnter preset ID to update: "))
                valid_id = [p[0] for p in presets]

                if preset_id not in valid_id:
                    print("Invalid preset ID")
                    input("Press enter to return to the main menu...")
                    continue

                # retrieve current preset info
                current = [p for p in presets if p[0] == preset_id][0]

                print(f"Current Values:")
                print(f"    Name: {current[1]}")
                print(f"    Balance: {current[2]:,.2f}")
                print(f"    Risk: {current[3]}%")
                print("\n leave blank / skip to keep current value")

                # get new values (or none if skipped)
                new_name = input("\nEnter new account name (or Enter to skip): ").strip()
                new_name = new_name if new_name else None

                new_balance = get_optional_number_input("\nEnter account balance (or Enter to skip): ")

                new_risk = get_optional_number_input("\nEnter new risk percentage (or Enter to skip): ")

                update_preset(preset_id, new_name, new_balance, new_risk)

                input("Press enter to return to the main menu...")

            except ValueError:
                print("Invalid preset ID")
                input("Press enter to return to the main menu...")

        elif option == "6": # delete a preset
            print(" ")
            display_all_presets()

            presets = get_all_presets()
            if not presets:
                input("\nPress Enter to return to the main menu...")
                continue

            while True:
                try:
                    preset_id = int(input("\nEnter preset ID: "))

                    valid_id = [p[0] for p in presets]

                    if preset_id in valid_id:
                        delete_preset(preset_id)
                        break
                    else:
                        print("Preset ID not found")
                except ValueError:
                    print("Invalid preset ID!")

            input("\nPress enter to return to main menu...")

        elif option == "7": # exit program
            print("\nThank you for using hxxis's position size calculator")
            break
        else:
            print("\nInvalid input! please enter a number!")

if __name__ == "__main__":
    main()