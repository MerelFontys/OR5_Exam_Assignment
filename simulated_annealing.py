#Simulated annealing
#Imports 
import random as r
import pandas as pd 
import math as m
import herbruikbare_functies as hf

#Dataset inladen
orders = pd.read_excel("PaintShop - November 2026.xlsx" , sheet_name = "Orders")
machines = pd.read_excel ("PaintShop - November 2026.xlsx" , sheet_name="Machines")
setups = pd.read_excel ("PaintShop - November 2026.xlsx" , sheet_name="Setups")

orders_info = orders.to_dict("records")

'''Random eerste oplossing kiezen'''
def random_initial_solution(orders, machines):
    #lege schedule maken
    schedule = {}   

    #machinenamen een lijst van maken
    machine_names = machines ["Machine"].tolist()


    # lege lijsten maken
    for i in machine_names:
        schedule[i] = []

    # een lijst maken van orderids 
    order_ids = orders["Order"].tolist()

    # husselen
    r.shuffle(order_ids)

    # random verdelen
    for j in order_ids:
        gekozen_machine = r.choice(machine_names)
        schedule[gekozen_machine].append(j)

    return schedule

'''Swap neighbourhood'''
def swap_neighbourhood (schedule):
    #kopie maken
    new_schedule = schedule.copy()
    for i in new_schedule:
        new_schedule[i] = new_schedule[i].copy()
    #machines die niet leeg zijn (anders kunnen ze niet swappen)
    non_empty = []
    for i in new_schedule:
        if len(new_schedule[i])!=0:
            non_empty.append(i)
    #Als minder dan 2 machines taken hebben dan kan swappen niet
    if len(non_empty) < 2: 
        return new_schedule
    #swappen
    #machines kiezen om tussen te swappen
    machine1chosen = r.choice(non_empty)
    machine2chosen = r.choice(non_empty)
    #kan sample ook 2x hetzelfde getal geven
    

    #orders van desbetreffende machines kiezen om te swappen
    order1 = r.choice(new_schedule[machine1chosen])
    order2 = r.choice(new_schedule[machine2chosen])

    #indexen krijgen van orders die geswapt worden 
    index1 = new_schedule[machine1chosen].index(order1)
    index2 = new_schedule[machine2chosen].index(order2)

    #daadwerkelijk swappen
    new_schedule[machine1chosen][index1]=order2
    new_schedule[machine2chosen][index2]=order1

    return new_schedule

'''Simulated Annealing'''
def simulated_annealing (orders, machines, setups, start_temp, end_temp, cooling, max_iterations):
    #beginoplossing
    current_solution = random_initial_solution(orders, machines)
    current_completion = hf.calculate_completion_times(current_solution, machines, setups)
    current_tardiness = hf.calculate_total_tardiness (orders_info , current_completion)

    #beste oplossingen aanmaken en zetten aan eerste oplossing
    best_solution = current_solution
    best_tardiness = current_tardiness 
    T = start_temp

    #visualisatie data
    current_objective_history = []
    best_objective_history = []
    temperature_history = []
    run_number = []
    for i in range (max_iterations):
        #buur aanmaken
        neighbour = swap_neighbourhood(current_solution)

        #tardiness van die buur
        neighbour_completion = hf.calculate_completion_times (neighbour, machines, setups)
        neighbour_tardiness = hf.calculate_total_tardiness(orders_info , neighbour_completion)
        
        #verschil tussen neighbour en huidige oplossing
        difference = neighbour_tardiness - current_tardiness

        if difference < 0: 
            current_solution = neighbour 
            current_tardiness = neighbour_tardiness

            if neighbour_tardiness < best_tardiness:
                best_tardiness = neighbour_tardiness
                best_solution = neighbour
        else: 
            #alsnog soms accepteren
            prob = m.exp (-difference/T)
            if r.random() < prob: 
                    current_solution = neighbour 
                    current_tardiness = neighbour_tardiness   
        #af laten koelen
        T = T * cooling

        #Data toevoegen voor plot
        current_objective_history.append(current_tardiness)
        best_objective_history.append(best_tardiness)
        temperature_history.append(T)
        run_number.append(i)

        #Voortgang printen 
        print(f'Iteration = {i} Temperature = {T:.4f} Current Tardiness = {current_tardiness:.4f} Best Tardiness {best_tardiness:.4f}')
        if T < end_temp: 
            break
    return (best_solution, best_tardiness, current_objective_history, best_objective_history, temperature_history, run_number) 


best_solution, best_tardiness, current_objective_history, best_objective_history, temperature_history, run_number = simulated_annealing(orders, machines, setups, start_temp = 100000, end_temp = 0.01, cooling = 0.99, max_iterations=100000000000)

print(f'best solution = {best_solution} \nbest tardiness = {best_tardiness}')


