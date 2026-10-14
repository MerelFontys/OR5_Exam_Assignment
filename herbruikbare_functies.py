import pandas as pd

# Functies om later te gebruiken
def get_machine(machines, name):
    return machines[machines["Machine"] == name].iloc[0]
'''filter de tabel door alleen de machine te pakken waar de naam matcht'''

def get_setup_time(from_colour, to_colour, setups):
    match = setups[(setups["From colour"] == from_colour) & (setups["To colour"] == to_colour)]
    return match.iloc[0]["Setup time"]
'''maakt het makkelijker om de wisseltijden van de verfkleuren op te halen'''

def processing_time(order, machine_row): 
    return order['Surface'] / machine_row['Speed']
'''hoeveel verwerkingstijd order x nodig heeft op machine y.
is afhankelijk van oppervlak van order en snelheid van machine'''

def calculate_completion_times(schedule, machines, setup_times, orders_info): # schedule is dan een dictionary met machine_naam: [lijst met orders in volgorde]
    completion_times = {} # maak een dictionary met hoelang elke order duurt met afronden
    for name, order_sequence in schedule.items(): # bereken data voor alle orders (in volgorde van schedule) per machine
        machine = get_machine(machines, name)

        current_time = 0 
        previous_colour = None 

        for order_id in order_sequence: 
            order = next(ord for ord in orders_info if ord['Order'] == order_id)

            if previous_colour is not None and previous_colour != order['Colour']:
                current_time += get_setup_time(previous_colour, order['Colour'], setups=setup_times)

            current_time += processing_time(order, machine)
            completion_times[order_id] = current_time # voeg de completion time van die order toe aan een dictionary
            previous_colour = order['Colour']
    return completion_times
'''
berekent hoelang elke order duurt met afronden volgens een bepaald schedule
de output is dan hoelang het in totaal duurt totdat de order is afgerond
ook wel: starttijd + verwerkingstijd
'''

def calculate_total_tardiness(orders_info, completion_times): 
    total_tardiness = 0
    for order in orders_info: 
        order_id = order['Order']
        tardiness_order = max(0, completion_times[order_id] - order['Deadline'])
        total_tardiness += tardiness_order
    return total_tardiness
'''
berekent hoeveel tijd er zit tussen de tijd van afronden en de eigenlijke deadline.
ook wel afronding - deadline
0 als afronding < deadline
'''

def calculate_penalty_cost(orders_info, completion_times): 
    total_cost = 0
    for order in orders_info: 
        order_id = order['Order']
        cost_order = max(0, completion_times[order_id] - order['Deadline']) * order['Penalty']
        total_cost += cost_order
    return total_cost
'''
bijbehorende penalty | hoeveel te laat * hoeveel "strafpunten"
'''



# ----------------------------------------------------------------------------------------------------------------------------
# Alle data voor de schedule in excel   
def schedule_data(schedule, orders_info, machines, setups): 
    # Roep schedule aan en pak alle dictionaries
    # schedule, seq_numbers, time_setup, starttimes, processingtimes, completion_times, machine_assigned = g.greedy_schedule(orders_info, machines, setups)
    
    rows = []

    for machine_name in schedule: 
        machine = get_machine(machines, machine_name)
        current_time = 0 
        previous_colour = None
        seq_no = 0

        for order_id in schedule[machine_name]:
            order = next(ord for ord in orders_info if ord['Order']==order_id)
            seq_no += 1
            setup = 0 
            if previous_colour is not None and previous_colour != order['Colour']:
                setup = get_setup_time(previous_colour, order['Colour'], setups)

            starttime = current_time + setup
            procestime = processing_time(order, machine)
            endtime = starttime + procestime

            deadline = order['Deadline']
            penalty_rate = order['Penalty']
            tardiness = max(0, endtime - deadline)
            cost = tardiness * penalty_rate

            rows.append({
                "Order": order_id,
                "Machine": machine_name,
                "SeqNo": seq_no,
                "Setup": setup,
                "Start": starttime,
                "Process": procestime,
                "End": endtime,
                "Deadline": deadline,
                "Tardiness": tardiness,
                "Penalty": penalty_rate,
                "Cost": cost
            })

            current_time = endtime
            previous_colour = order['Colour']

    return rows
'''
maakt alle rijen aan zodat er daarna een Excel file van gemaakt kan worden
'''

# Excel file met schedule exporteren
def export_schedule(schedule_data, filename='Paintshop_Schedule_September.xlsx'): 
    data_file = pd.DataFrame(schedule_data, columns=[
        "Order", "Machine", "SeqNo", "Setup", "Start", "Process", 
        "End", "Deadline", "Tardiness", "Penalty", "Cost"
    ])
    data_file.to_excel(filename, sheet_name='Schedule', index=False)