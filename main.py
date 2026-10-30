import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g
import improving_search as im
import validatie as v
from pathlib import Path
import simulated_annealing as sa 
import visualisatie as vi

def main(): 
    # Validaties
    print(f"\n {v.planning_by_code=} \n {v.planning_by_hand=}")
    if v.planning_by_code == v.planning_by_hand:
        print("\n Het genereren van de greedy planning is gevalideerd")
    else:
        print('Er gaat iets fout in het genereren van de greedy planning')
    
    # Inladen van de tabellen uit de excel file
    datafile = "PaintShop - September 2026.xlsx" # Hier: aanpassen dataset naam
    orders = pd.read_excel(datafile, sheet_name = 'Orders')
    machines = pd.read_excel(datafile, sheet_name = 'Machines')
    setups = pd.read_excel(datafile, sheet_name = 'Setups')
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
    print('\n Discrete Improving Search aan het laden... Dit kan even duren')

    # -------------------------------
    # Stats Discrete Improved Search (Insertion)
    improved_greedy_schedule = im.improving_search(greedy_heur_sched, machines, setups, orders_info)[0]
    improved_grd_comp_times = h.calculate_completion_times(improved_greedy_schedule, machines, setups, orders_info)
    total_tardiness_imp_grd = h.calculate_total_tardiness(orders_info, improved_grd_comp_times)
    total_cost_imp_grd = h.calculate_penalty_cost(orders_info, improved_grd_comp_times)

    print('\n Improved Search Greedy (insertion)') # Print de machine schedule
    print(f'     {total_tardiness_imp_grd = :.2f}') # Print de total tardiness
    print(f'     {total_cost_imp_grd = :.2f} \n') # Print de total cost in penalties

    # Verbetering
    print(f"Na de improving search is de oplossing in verhouding {(abs(total_tardiness_imp_grd - total_cost_penalties)/total_cost_penalties)*100:.2f}% verbeterd! \n")

    best_solution, best_tardiness, best_penalty, current_objective_history, best_objective_history, temperature_history, run_number = sa.simulated_annealing(orders, machines, setups, 
                                                                                                                                                          start_temp = 100_000_000, 
                                                                                                                                                          end_temp = 0.001, 
                                                                                                                                                          cooling = 0.99, 
                                                                                                                                                          max_iterations=1000000)

    improved_sa_schedule = im.improving_search(best_solution, machines, setups, orders_info)[0]
    improved_sa_comp_times = h.calculate_completion_times(improved_sa_schedule, machines, setups, orders_info)
    total_tardiness_improved_sa = h.calculate_total_tardiness(orders_info, improved_sa_comp_times)
    total_cost_improved_sa = h.calculate_penalty_cost(orders_info, improved_sa_comp_times)
    print(f'Improved Search SA {total_cost_improved_sa = :.2f}')

    #visualisaties simulated annealing
    #simulated annealing progressie 
    vi.plot_sa_progress(current_objective_history, best_objective_history, run_number)
    #gannt chart 
    schedule_data = sa.best_schedule_sa_data
    vi.plot_schedule(schedule_data)
      
    
    # -------------------------------
    # exporteren van excel file ----- probleem? -> Windows R --> C:\Users\Merel\ --> november
    # optimale schedule
    print(f"\n {total_cost_improved_sa = :.2f}, {total_cost_imp_grd = :.2f}")
    if total_cost_improved_sa < total_cost_imp_grd:
        data = h.schedule_data(improved_sa_schedule, orders_info, machines, setups)
        print(f"De improved schedule van simulated annealing is beter dan de improved schedule van greedy met een verschil van {total_cost_imp_grd - total_cost_improved_sa:.2f} in kosten")
    if total_cost_improved_sa > total_cost_imp_grd:
        data = h.schedule_data(improved_greedy_schedule, orders_info, machines, setups)
        print(f"De improved schedule van greedy is beter dan de improved schedule van simulated annealing met een verschil van {total_cost_improved_sa - total_cost_imp_grd:.2f} in kosten")

    output_path = Path(__file__).parent / "Paintshop_Schedule_September.xlsx"
    h.export_schedule(data, output_path)
    print(f"Opgeslagen als: {output_path} \n Als de file niet in de map staat: Windows + R met c:\\Users\\Merel\\Paintshop_Schedule_September.xlsx \n")

if __name__ == "__main__":
    main()
