import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g
import random

'''
voor nu greedy, maar pas alles aan naar beste manier 
'''

orders = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Orders')
machines = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Machines')
setups = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Setups')
orders_info = orders.to_dict('records')

def improving_search(schedule, machines, setups, orders_info): 
    completion_times = h.calculate_completion_times(schedule, machines, setups)
    best_cost = h.calculate_penalty_cost(orders_info, completion_times)


    ''' Sander local optimum voor andere stop!!!!!! Dit hou ik nu aan zelf:'''

    iterations = 0 # temp stopconditie
    improved_this_round = True # Hij stopt wanneer er in een ronde geen verbeteringen meer zijn
    
    while improved_this_round:
        improved_this_round = False

        best_schedule = schedule
        best_cost_this_round = best_cost
        
        for from_machine in schedule: 
            for i in range(len(schedule[from_machine])):
                order = schedule[from_machine][i]

                # check alleen 1 random machine ipv ze allemaal --> sneller
                other_machines = [m for m in schedule if m != from_machine]
                other_chosen = random.choice(other_machines)
                machines_to_check = [from_machine, other_chosen]
        
                for to_machine in machines_to_check: 
                    for j in range(len(schedule[to_machine]) + 1):
                            
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
        
                        if possible_cost < best_cost_this_round: # je bekijkt alle posities en onthoud 'm alleen als hij beter is dan alle andere mogelijkheden tot nu toe
                            best_cost_this_round = possible_cost
                            best_schedule = new_schedule
                            improved_this_round = True
        
        schedule = best_schedule  # als alle mogelijkheden zijn doorlopen, past het schema aan
        new_cost = best_cost_this_round

        '''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''
        iterations += 1 # temp stopconditie
        if iterations > 5:
            improved_this_round = False
        
    return schedule, new_cost