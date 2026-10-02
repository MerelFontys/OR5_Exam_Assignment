import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g

'''
voor nu greedy, maar pas alles aan naar beste manier 
'''

orders = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Orders')
machines = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Machines')
setups = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Setups')
orders_info = orders.to_dict('records')

def improving_search(schedule, machines, setups, orders_info): 
    completion_times = h.calculate_completion_times(schedule, machines, setups)
    cost_start_search = h.calculate_penalty_cost(orders_info, completion_times)
    
    improved = False
    temp_best_cost = cost_start_search

    for from_machine in schedule: 
        for i in range(len(schedule[from_machine])):
            order = schedule[from_machine][i]

            for to_machine in schedule: 
                for j in range(len(schedule[to_machine]) + 1):

                    if from_machine == to_machine and j == i: # zelfde plek als waar die al staat
                        continue
                    
                    new_schedule = {}
                    for m in schedule:
                        new_schedule[m] = schedule[m].copy()
                    
                    new_schedule[from_machine].pop(i) # verwijderen van de order die weg is van die machine

                    insertion_place = j 
                    if from_machine == to_machine and j > i: 
                        insertion_place = j-1

                    new_schedule[to_machine].insert(insertion_place, order)
                    new_completion_times = h.calculate_completion_times(new_schedule, machines, setups)
                    possible_cost = h.calculate_penalty_cost(orders_info, new_completion_times)

                    if possible_cost < temp_best_cost: 
                        temp_best_cost = possible_cost
                        best_schedule = new_schedule
                        improved = True

        schedule = best_schedule 
        new_cost = temp_best_cost

    return schedule, new_cost, improved