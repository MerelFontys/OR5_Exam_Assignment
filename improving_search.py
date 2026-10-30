
import pandas as pd
import herbruikbare_functies as h
import random as r


def improving_search(schedule, machines, setups, orders_info):
    """
    Discrete Improving Search met een beperkte buurruimte.

    Per order worden de invoegposities op de eigen machine en
    één willekeurig gekozen andere machine onderzocht.
    De beste verbetering van een ronde wordt geaccepteerd.

    De functie stopt wanneer een volledige ronde geen verbetering
    vindt binnen de onderzochte buurruimte.
    """
    completion_times = h.calculate_completion_times(schedule, machines, setups, orders_info)
    best_cost = h.calculate_penalty_cost(orders_info, completion_times)
    r.seed(2)  # Maakt de keuzes reproduceerbaar elke keer dezelfde seed betekent elke keer dezelfde "random" keuzes
    improved_this_round = True
    while improved_this_round:
        #zet improved this round naar false dat als er geen verbetering is dat de whileloop breekt
        improved_this_round = False
        best_schedule = schedule
        best_cost_this_round = best_cost

        for from_machine in schedule:
            for i in range(len(schedule[from_machine])):
                order = schedule[from_machine][i]
                other_machines = []
                # Kies één andere machine
                for machine in schedule:
                    if machine != from_machine:
                        other_machines.append(machine)
                machines_to_check = []
                machines_to_check.append(from_machine)
                if len (other_machines) > 0:
                    other_chosen = r.choice(other_machines)
                    machines_to_check.append(other_chosen)
                for to_machine in machines_to_check:
                    for j in range(len(schedule[to_machine]) + 1):

                        # Maak een kopie van de huidige planning
                        new_schedule ={}
                        for machine in schedule:
                            new_schedule[machine] = schedule[machine].copy()

                        # Verwijder de order van de oorspronkelijke machine
                        new_schedule[from_machine].pop(i)
                        insertion_place = j
                        # Corrigeer de positie als de order op dezelfde
                        # machine naar een latere positie wordt verplaatst
                        if from_machine == to_machine and j > i:
                            insertion_place = j - 1

                        # Voeg de order op de nieuwe positie in
                        new_schedule[to_machine].insert(insertion_place, order)

                        # Bereken de penaltykosten van de nieuwe planning
                        new_completion_times = h.calculate_completion_times(new_schedule, machines, setups, orders_info)
                        possible_cost = h.calculate_penalty_cost(orders_info, new_completion_times)
                        # validatie buuroplossing: print("order", order, "van", from_machine, "naar", to_machine, "positie", insertion_place)

                        # Bewaar de beste verbetering van deze ronde
                        if possible_cost < best_cost_this_round:
                            best_cost_this_round = possible_cost
                            best_schedule = new_schedule
                            improved_this_round = True

        # Accepteer de beste verbetering van deze ronde
        schedule = best_schedule
        best_cost = best_cost_this_round

    return schedule, best_cost


def improving_search_bigger_neighbourhood(schedule, machines, setups, orders_info):
    """
    Discrete Improving Search met een grotere buurruimte.

    Voor iedere order worden de invoegposities op alle machines
    onderzocht. De beste verbetering van een ronde wordt geaccepteerd.

    De functie stopt wanneer een volledige ronde geen verbetering
    vindt. Dan is de oplossing lokaal optimaal ten opzichte van
    alle onderzochte insertion moves.
    """

    completion_times = h.calculate_completion_times(schedule, machines, setups, orders_info)
    best_cost = h.calculate_penalty_cost(orders_info, completion_times)
    improved_this_round = True

    while improved_this_round:
        improved_this_round = False
        best_schedule = schedule
        best_cost_this_round = best_cost

        for from_machine in schedule:
            for i in range(len(schedule[from_machine])):
                order = schedule[from_machine][i]

                # Onderzoek alle machines
                for to_machine in schedule:
                    for j in range(len(schedule[to_machine]) + 1):

                        # Maak een kopie van de huidige planning
                        new_schedule = {}
                        for machine in schedule:
                            new_schedule[machine] = schedule[machine].copy()

                        # Verwijder de order van de oorspronkelijke machine
                        new_schedule[from_machine].pop(i)
                        insertion_place = j

                        # Corrigeer de positie bij verplaatsen op dezelfde machine
                        if from_machine == to_machine and j > i:
                            insertion_place = j - 1

                        # Voeg de order op de nieuwe positie in
                        new_schedule[to_machine].insert(insertion_place, order)

                        # Bereken de penaltykosten van de nieuwe planning
                        new_completion_times = h.calculate_completion_times(new_schedule, machines, setups, orders_info)
                        possible_cost = h.calculate_penalty_cost(orders_info, new_completion_times)

                        # Bewaar de beste verbetering van deze ronde
                        if possible_cost < best_cost_this_round:
                            best_cost_this_round = possible_cost
                            best_schedule = new_schedule
                            improved_this_round = True

        # Accepteer de beste verbetering van deze ronde
        schedule = best_schedule
        best_cost = best_cost_this_round

    return schedule, best_cost

