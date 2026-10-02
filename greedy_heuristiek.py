# Import statements
import math as m
import pandas as pd
import herbruikbare_functies as h


# ----------------------------------------------------------------------------------------------------------------------------
# Greedy constructive heuristic --> Earliest Due Date (EDD)
def greedy_schedule(orders_info, machines, setup_times):
    edd = sorted(orders_info, key=lambda order: order["Deadline"]) # maak een begin volgorde op basis van EDD

    free_at_time = {}
    previous_colour = {}
    schedule = {}
    # dictionaries per order_id
    completion_times = {}
    seq_numbers = {}
    time_setup = {}
    starttimes = {}
    processingtimes ={}
    machine_assigned = {}
    duration = {}

    machine_names = machines["Machine"].tolist()
    
    for machine in machine_names: 
        free_at_time[machine] = 0 
        previous_colour[machine] = None
        schedule[machine] = []

    for order in edd:
        order_id = order['Order'] 
        colour = order['Colour'] 
        temp_starting_times = {}

        for machine in machine_names: 
            if previous_colour[machine] is None or previous_colour[machine] == colour:
                colour_change = 0
            else:  
                colour_change = h.get_setup_time(previous_colour[machine], colour, setup_times)
            # time_setup[order_id] = colour_change
            temp_starting_times[machine] = free_at_time[machine] + colour_change
            # starttimes[order_id] = temp_starting_times[chosen]
        
        chosen = min(temp_starting_times, key=temp_starting_times.get)

        if previous_colour[chosen] is None or previous_colour[chosen] == colour:
            actual_setup = 0
        else:
            actual_setup = h.get_setup_time(previous_colour[chosen], colour, setup_times)

        time_setup[order_id] = actual_setup
        starttimes[order_id] = temp_starting_times[chosen]

        machine_row = h.get_machine(machines, chosen)
        duration = h.processing_time(order, machine_row)
        schedule[chosen].append(order_id) 
        seq_numbers[order_id] = len(schedule[chosen])
        free_at_time[chosen] = starttimes[order_id] + duration
        completion_times[order_id] = free_at_time[chosen]
        previous_colour[chosen] = colour
        machine_assigned[order_id] = chosen

    return schedule, seq_numbers, time_setup, starttimes, processingtimes, completion_times, machine_assigned