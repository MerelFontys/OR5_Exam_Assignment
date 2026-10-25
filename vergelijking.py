
import pandas as pd
import random as r
import time
import herbruikbare_functies as h
import greedy_heuristiek as greedy
import improving_search as dis
from simulated_annealing import orders_info 
from simulated_annealing import simulated_annealing


df = "Paintshop - September 2026.xlsx"
print("de code runt, duurt alleen een halfuur om volledig te runnen")

orders = pd.read_excel(df,sheet_name="Orders")
machines = pd.read_excel(df,sheet_name="Machines")
setups = pd.read_excel(df,sheet_name="Setups")
orders_info = orders.to_dict("records")


# 2. Instellingen simulated annealing


number_of_runs = 10
start_temp = 100_000_000
end_temp = 0.001
cooling = 0.99
max_iterations = 10000



def calculate_cost(schedule):
    completion_times = h.calculate_completion_times(schedule,machines,setups,orders_info)
    cost = h.calculate_penalty_cost(orders_info,completion_times)
    return cost



#Functie om DIS uit te voeren


def run_dis(schedule, machines, setups, orders_info):
    return dis.improving_search_bigger_neighbourhood(
        schedule,
        machines,
        setups,
        orders_info
    )
#Greedy constructive heuristiek

start = time.perf_counter()
greedy_result = greedy.greedy_schedule(orders_info,machines, setups)
greedy_schedule = greedy_result[0]
greedy_time = time.perf_counter() - start
# Penaltykosten vóór DIS
greedy_cost_before = calculate_cost(greedy_schedule)

# DIS uitvoeren
start = time.perf_counter()

greedy_final_schedule, greedy_cost_after = run_dis(
    greedy_schedule,
    machines,
    setups,
    orders_info
)

greedy_dis_time = time.perf_counter() - start
greedy_results = {
    "Methode": "Greedy",
    "Run": 1,
    "Penalty vóór DIS": greedy_cost_before,
    "Penalty na DIS": greedy_cost_after,
    "Tijd methode (sec)": greedy_time,
    "Tijd DIS (sec)": greedy_dis_time,
    "Totale tijd (sec)": greedy_time + greedy_dis_time
}



# 6. Simulated annealing: meerdere onafhankelijke runs


sa_results = []
print("Simulated annealing wordt gestart...")
for run in range(number_of_runs):
    # Elke run krijgt een eigen seed anders is alles hetzelfde, maar nu is het wel nog reproduceerbaar
    r.seed(run)
    start = time.perf_counter()
    sa_result = simulated_annealing(
        orders,
        machines,
        setups,
        start_temp=start_temp,
        end_temp=end_temp,
        cooling=cooling,
        max_iterations=max_iterations
    )

    sa_time = time.perf_counter() - start

    # De beste planning uit simulated annealing
    sa_schedule = sa_result[0]
    # Penaltykosten vóór DIS
    sa_cost_before = calculate_cost(sa_schedule)
    # DIS uitvoeren
    start = time.perf_counter()
    sa_final_schedule, sa_cost_after = run_dis(
        sa_schedule,
        machines,
        setups,
        orders_info
    )
    dis_time = time.perf_counter() - start

    # Resultaten van deze run opslaan
    sa_results.append({
        "Methode": "Simulated annealing",
        "Run": run + 1,
        "Penalty vóór DIS": sa_cost_before,
        "Penalty na DIS": sa_cost_after,
        "Tijd methode (sec)": sa_time,
        "Tijd DIS (sec)": dis_time,
        "Totale tijd (sec)": sa_time + dis_time
    })

    print(
        f"SA-run {run + 1}/{number_of_runs}: "
        f"penalty vóór DIS = {sa_cost_before:.2f}; "
        f"na DIS = {sa_cost_after:.2f}; "
        f"totale tijd = {sa_time + dis_time:.2f} sec"
    )

#samenvoegen van resultaten

all_results = pd.DataFrame(
    [greedy_results] + sa_results
)

#resultaten samenvatten

summary_rows = []
for method in ["Greedy", "Simulated annealing"]:
    subset = all_results[all_results["Methode"] == method]
    for i in [
        "Penalty vóór DIS",
        "Penalty na DIS",
        "Tijd methode (sec)",
        "Tijd DIS (sec)",
        "Totale tijd (sec)"
    ]:
        values = subset[i]

        summary_rows.append({
            "Methode": method,
            "Maatstaf": i,
            "Beste/laagste": values.min(),
            "Gemiddelde": values.mean(),
            "Standaarddeviatie": (
                values.std(ddof=1) if len(values) > 1 else 0.0
            )
        })

summary = pd.DataFrame(summary_rows)

#resultaten weergeven

print(" RESULTATEN PER RUN ")
print(all_results.round(2).to_string(index=False), flush=True)
print(" SAMENVATTING ", )
print(summary.round(2).to_string(index=False),flush  =True)
print("Alle berekeningen zijn klaar.")

