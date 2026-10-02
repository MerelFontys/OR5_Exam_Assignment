import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g
import improving_search as im
# import validatie as v
# import werkruimte_sander
from pathlib import Path


def main():
    # Inladen van de tabellen uit de excel file
    orders = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Orders')
    machines = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Machines')
    setups = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Setups')
    orders_info = orders.to_dict('records')

    # -------------------------------
    # Stats greedy constructieve heuristiek EDD
    greedy_heur_sched = g.greedy_schedule(orders_info, machines, setups)[0]
    greedy_heur_comp_times = g.greedy_schedule(orders_info, machines, setups)[5]
    total_tardiness_greedy = h.calculate_total_tardiness(orders_info, greedy_heur_comp_times)
    total_cost_penalties = h.calculate_penalty_cost(orders_info, greedy_heur_comp_times)

    print('\n Greedy') # Print de machine schedule
    print(f'     {total_tardiness_greedy = :.2f}') # Print de total tardiness
    print(f'     {total_cost_penalties = :.2f}') # Print de total cost in penalties
    print('De Discrete Improving Search aan het laden... Dit kan even duren (20sec)')

    # -------------------------------
    # Stats Discrete Improved Search (Insertion)
    improved_greedy_schedule = im.improving_search(greedy_heur_sched, machines, setups, orders_info)[0]
    improved_grd_comp_times = h.calculate_completion_times(improved_greedy_schedule, machines, setups)
    total_tardiness_imp_grd = h.calculate_total_tardiness(orders_info, improved_grd_comp_times)
    total_cost_imp_grd = h.calculate_penalty_cost(orders_info, improved_grd_comp_times)

    print('\n Improved Greedy (insertion)') # Print de machine schedule
    print(f'     {total_tardiness_imp_grd = :.2f}') # Print de total tardiness
    print(f'     {total_cost_imp_grd = :.2f}') # Print de total cost in penalties

    # -------------------------------
    # Stats Discrete Improved Search (Insertion)
    double_imp_schedule = im.improving_search(improved_greedy_schedule, machines, setups, orders_info)[0]
    double_imp_comp_times = h.calculate_completion_times(double_imp_schedule, machines, setups)
    total_tardiness_double_improved = h.calculate_total_tardiness(orders_info, double_imp_comp_times)
    total_cost_double_improved = h.calculate_penalty_cost(orders_info, double_imp_comp_times)

    print('\n Double Improved (insertion)') # Print de machine schedule
    print(f'     {total_tardiness_double_improved = :.2f}') # Print de total tardiness
    print(f'     {total_cost_double_improved = :.2f} \n') # Print de total cost in penalties

    # exporteren van excel file ----- probleem? -> Windows R --> C:\Users\Merel\ --> november
    output_path = Path(__file__).parent / "Paintshop_Schedule_November.xlsx"
    data = h.schedule_data(orders_info, machines, setups)
    h.export_schedule(data, output_path)
    print(f"Opgeslagen als: {output_path} \n Als de file niet in de map staat: Windows + R met c:\\Users\\Merel\\Paintshop_Schedule_November.xlsx \n")

    

if __name__ == "__main__":
    main()
