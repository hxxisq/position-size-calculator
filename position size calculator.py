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

def main():
    print('POSITION SIZE CALCULATOR')

    while True:
        #get user input
        account_balance = get_number_input("\nAccount balance($): ")
        risk_percent = get_number_input("Risk percent(%): ")
        stop_loss = get_number_input("Stop loss(pips): ")

        #calculate lots size
        result = calculate_lot_size(account_balance, risk_percent, stop_loss)

        #display result
        print(f"Risk: ${result['risk_amount']}\nMini lot: {result['mini_lots']}")

        #ask if user wants to calculate again
        repeat = input("\nWant to calculate again? (y/n) ").lower()
        if repeat != "y":
            break

if __name__ == '__main__':
    main()