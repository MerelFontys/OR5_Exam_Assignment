import pandas as pd
import greedy_heuristiek as g

# Validatie generalisatie code (testen op verschillende datasets)
# Handmatig aanpassen van de bestandsnaam

# Validatie functies/berekeningen (testen op kleine dataset)
test_data = "PaintShop - Test.xlsx"
orders = pd.read_excel(test_data, sheet_name = 'Orders')
machines = pd.read_excel(test_data, sheet_name = 'Machines')
setups = pd.read_excel(test_data, sheet_name = 'Setups')
orders_info = orders.to_dict('records')

planning_by_hand = {'M1': ['O3'], 'M2': ['O1', 'O2']}
planning_by_code = g.greedy_schedule(orders_info, machines, setups)[0]
# verder in main


# ----- rest in schedule checker -----
