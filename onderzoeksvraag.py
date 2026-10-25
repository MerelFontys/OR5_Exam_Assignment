import pandas as pd
import time
import copy
import herbruikbare_functies as h
import greedy_heuristiek as g
import improving_search as im

naam_datafile = "Paintshop - September 2026.xlsx"


def onderzoeksvraag(datafile):

    
    # Dataset inladen
    orders = pd.read_excel(datafile, sheet_name="Orders")
    machines = pd.read_excel(datafile, sheet_name="Machines")
    setups = pd.read_excel(datafile, sheet_name="Setups")

    orders_info = orders.to_dict("records")

    # Greedy beginoplossing maken
    greedy_schedule = g.greedy_schedule(orders_info, machines, setups)[0]

    # Penaltykosten van de beginoplossing berekenen
    completion_times = h.calculate_completion_times(greedy_schedule, machines, setups, orders_info)

    penalty_before = h.calculate_penalty_cost(orders_info, completion_times)

    print(f"\nPenaltykosten voor DIS: {penalty_before:.2f}")

    #beperkte buurruimte
    schedule_limited = copy.deepcopy(greedy_schedule)
    start_time = time.perf_counter()
    improved_limited = im.improving_search(schedule_limited, machines, setups, orders_info)[0]
    time_limited = time.perf_counter() - start_time
    completion_limited = h.calculate_completion_times(improved_limited, machines, setups, orders_info)
    penalty_limited = h.calculate_penalty_cost(orders_info, completion_limited)
    if penalty_before !=0 :
        improvement_limited =((penalty_before - penalty_limited) / penalty_before) * 100
    else:
        improvement_limited = 0

    
    #grote buurruimte
    schedule_large = copy.deepcopy(greedy_schedule)
    start_time = time.perf_counter()
    improved_large = im.improving_search_bigger_neighbourhood(schedule_large, machines, setups, orders_info)[0]
    time_large = time.perf_counter() - start_time
    completion_large = h.calculate_completion_times(improved_large, machines, setups, orders_info)
    penalty_large = h.calculate_penalty_cost(orders_info, completion_large)
    if penalty_before != 0:
        improvement_large = (((penalty_before - penalty_large) / penalty_before) * 100)
    else:
        improvement_large = 0

    #Resultaten 

    print("\nBeperkte buurruimte:")
    print(f"Penalty voor DIS: {penalty_before:.2f}")
    print(f"Penalty na DIS: {penalty_limited:.2f}")
    print(f"Verbetering: {improvement_limited:.2f}%")
    print(f"Rekentijd: {time_limited:.2f} seconden")

    print("\nGrote buurruimte:")
    print(f"Penalty voor DIS: {penalty_before:.2f}")
    print(f"Penalty na DIS: {penalty_large:.2f}")
    print(f"Verbetering: {improvement_large:.2f}%")
    print(f"Rekentijd: {time_large:.2f} seconden")

    resultaten = [
        {
            "Dataset": datafile,
            "Buurruimte": "Beperkt",
            "Penalty voor DIS": penalty_before,
            "Penalty na DIS": penalty_limited,
            "Verbetering (%)": improvement_limited,
            "Rekentijd (seconden)": time_limited
          },
        {
            "Dataset": datafile,
            "Buurruimte": "Groot",
            "Penalty voor DIS": penalty_before,
            "Penalty na DIS": penalty_large,
            "Verbetering (%)": improvement_large,
            "Rekentijd (seconden)": time_large
        }
    ]
    return resultaten


# Beide datasets onderzoeken
alle_resultaten = []
#extend voegt alle dingen toe uit die lijst 
alle_resultaten.extend(onderzoeksvraag("PaintShop - September 2026.xlsx"))
alle_resultaten.extend(onderzoeksvraag("PaintShop - November 2026.xlsx"))

# Resultaten in een tabel zetten voor leesbaarheid
resultaten_df = pd.DataFrame(alle_resultaten)
print(resultaten_df)



