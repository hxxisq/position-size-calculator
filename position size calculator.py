account_balance = 10000
risk_percent = 1
stop_loss_pips = 50

risk_amount = account_balance * (risk_percent / 100)

pip_value = risk_amount / stop_loss_pips

mini_lot = pip_value / 1

print("...Lots Size Calculator...")
print(f"Account Balance: ${account_balance}")
print(f"Risk Percent: {risk_percent}%")
print(f"Stop Loss Pips: {stop_loss_pips} pips")
print(f"\nRisk Amount: ${risk_amount:,.2f}")
print(f"Mini lots size: {mini_lot:,.2f} lots")