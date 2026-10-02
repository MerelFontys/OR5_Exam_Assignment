import pandas as pd
import greedy_heuristiek as g

# Functies om later te gebruiken
def get_machine(machines, name): # filter de tabel door alleen die te pakken waar de naam matcht
    return machines[machines["Machine"] == name].iloc[0]

# Hoelang het duurt om te wisselen van ene kleur naar andere kleur
def get_setup_time(from_colour, to_colour, setups):
    match = setups[(setups["From colour"] == from_colour) & (setups["To colour"] == to_colour)]
    return match.iloc[0]["Setup time"]

# Hoeveel tijd order x nodig heeft op machine y | afhankelijk van oppervlak van order en snelheid van machine
def processing_time(order, machine_row): 
    return order['Surface'] / machine_row['Speed']

# Bereken hoelang elke order duurt met afronden volgens een bepaald schedule
def calculate_completion_times(schedule, machines, setup_times): # schedule is dan een dictionary met machine_naam: [lijst met orders in volgorde]
    completion_times = {} # maak een dictionary met hoelang elke order duurt met afronden
    for name, order_sequence in schedule.items(): # bereken data voor alle orders (in volgorde van schedule) per machine
        machine = get_machine(machines, name)

        current_time = 0 # de machine begint met tijd 0
        previous_colour = None # je begint zonder kleur

        for order_id in order_sequence: 
            order = next(ord for ord in orders_info if ord['Order'] == order_id)

            if previous_colour is not None and previous_colour != order['Colour']:
                current_time += get_setup_time(previous_colour, order['Colour'], setups=setup_times)

            current_time += processing_time(order, machine)
            completion_times[order_id] = current_time # voeg de completion time van die order toe aan een dictionary
            previous_colour = order['Colour']
    return completion_times

# Hoeveel tijd er zit tussen de tijd van afronden en de eigenlijke deadline | 0 als afronding < deadline
def calculate_total_tardiness(orders_info, completion_times): 
    total_tardiness = 0
    for order in orders_info: 
        order_id = order['Order']
        tardiness_order = max(0, completion_times[order_id] - order['Deadline'])
        total_tardiness += tardiness_order
    return total_tardiness

# Bijbehorende penalty | hoeveel te laat * hoeveel "strafpunten"
def calculate_penalty_cost(orders_info, completion_times): 
    total_cost = 0
    for order in orders_info: 
        order_id = order['Order']
        cost_order = max(0, completion_times[order_id] - order['Deadline']) * order['Penalty']
        total_cost += cost_order
    return total_cost


# ----------------------------------------------------------------------------------------------------------------------------
# Alle data voor de schedule in excel   
def schedule_data(orders_info, machines, setups): 
    # Roep schedule aan en pak alle dictionaries
    schedule, seq_numbers, time_setup, starttimes, processingtimes, completion_times, machine_assigned = g.greedy_schedule(orders_info, machines, setups)
    
    rows = []

    for order in orders_info:
        order_id = order['Order']
        
        endtime = completion_times.get(order_id, 0)
        deadline = order['Deadline']
        penalty_rate = order.get('Penalty', 0)
        
        tardiness = max(0, endtime - deadline)
        penalty = tardiness * penalty_rate
        cost = penalty

        rows.append({
            "Order": order_id,
            "Machine": machine_assigned.get(order_id),
            "SeqNo": seq_numbers.get(order_id),
            "Setup": time_setup.get(order_id, 0),
            "Start": starttimes.get(order_id, 0),
            "Process": processingtimes.get(order_id, 0),
            "End": endtime,
            "Deadline": deadline,
            "Tardiness": tardiness,
            "Penalty": penalty,
            "Cost": cost
        })
    return rows

# Excel file met scchedule exporteren
def export_schedule(schedule_data, filename='Paintshop_Schedule_November.xlsx'): 
    data_file = pd.DataFrame(schedule_data, columns=[
        "Order", "Machine", "SeqNo", "Setup", "Start", "Process", 
        "End", "Deadline", "Tardiness", "Penalty", "Cost"
    ])
    data_file.to_excel(filename, sheet_name='Schedule', index=False)