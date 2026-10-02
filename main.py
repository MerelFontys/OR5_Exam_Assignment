import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g
# import werkruimte_sander
from pathlib import Path

def main():
    # Inladen van de tabellen uit de excel file
    orders = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name = 'Orders')
    machines = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name = 'Machines')
    setups = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name = 'Setups')
    orders_info = orders.to_dict('records')

    # ----------------------------------------------------------------------------------------------------------------------------
    # wat random printen van EDD schedules op machines, completion times per order en check
    greedy_heur_sched = g.greedy_schedule(orders_info, machines, setups)[0]
    greedy_heur_comp_times = g.greedy_schedule(orders_info, machines, setups)[5]

    total_tardiness_greedy = h.calculate_total_tardiness(orders_info, greedy_heur_comp_times)
    total_cost_penalties = h.calculate_penalty_cost(orders_info, greedy_heur_comp_times)

    print('\n Schedule per machine') # Print de machine schedule
    for key, value in greedy_heur_sched.items():
        print(f"{key}: {value}")
    print(f'\n {total_tardiness_greedy = :.2f}') # Print de total tardiness
    print(f' \n {total_cost_penalties = :.2f} \n') # Print de total cost in penalties 

    # exporteren van excel file ----- probleem? -> Windows R --> C:\Users\Merel\ --> november
    output_path = Path(__file__).parent / "Paintshop_Schedule_November.xlsx"
    data = h.schedule_data(orders_info, machines, setups)
    h.export_schedule(data, output_path)
    print(f"Opgeslagen als: {output_path} \n")

if __name__ == "__main__":
    main()