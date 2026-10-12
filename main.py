import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g
import improving_search as im
import validatie as v
# import werkruimte_sander
from pathlib import Path


def main(): 
    # Validaties
    if v.validatie_greedy_schedule == v.handmatig_planning:
        print("\n Het genereren van de greedy planning is gevalideerd")
    else:
        print('Er gaat iets fout in het genereren van de greedy planning')
    
    # Inladen van de tabellen uit de excel file
    orders = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name = 'Orders')
    machines = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name = 'Machines')
    setups = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name = 'Setups')
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
    print('\n Discrete Improving Search aan het laden... Dit kan even duren (ongeveer 50sec op mijn laptop in ieder geval)')

    # -------------------------------
    # Stats Discrete Improved Search (Insertion)
    improved_greedy_schedule = im.improving_search_bigger_neighbourhood(greedy_heur_sched, machines, setups, orders_info)[0]
    improved_grd_comp_times = h.calculate_completion_times(improved_greedy_schedule, machines, setups, orders_info)
    total_tardiness_imp_grd = h.calculate_total_tardiness(orders_info, improved_grd_comp_times)
    total_cost_imp_grd = h.calculate_penalty_cost(orders_info, improved_grd_comp_times)

    print('\n Improved Search Greedy (insertion)') # Print de machine schedule
    print(f'     {total_tardiness_imp_grd = :.2f}') # Print de total tardiness
    print(f'     {total_cost_imp_grd = :.2f} \n') # Print de total cost in penalties

    # Verbetering
    print(f"Na de improving search is de oplossing in verhouding {(abs(total_tardiness_imp_grd - total_cost_penalties)/total_cost_penalties)*100:.2f}% verbeterd! \n")

    # -------------------------------
    # exporteren van excel file ----- probleem? -> Windows R --> C:\Users\Merel\ --> november
    output_path = Path(__file__).parent / "Paintshop_Schedule_September.xlsx"
    data = h.schedule_data(orders_info, machines, setups)
    h.export_schedule(data, output_path)
    print(f"Opgeslagen als: {output_path} \n Als de file niet in de map staat: Windows + R met c:\\Users\\Merel\\Paintshop_Schedule_September.xlsx \n")


if __name__ == "__main__":
    main()
