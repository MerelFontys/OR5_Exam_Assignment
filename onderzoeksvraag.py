import pandas as pd
import herbruikbare_functies as h
import greedy_heuristiek as g
import random
import improving_search as im

'''
voor nu greedy, maar pas alles aan naar beste manier 
'''

orders = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Orders')
machines = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Machines')
setups = pd.read_excel("PaintShop - November 2026.xlsx", sheet_name = 'Setups')
orders_info = orders.to_dict('records')

'''
allebei de improving searches runnen en de tijdsduur opslaan en de uitkomsten

- in welke mate levert het beperken van het aantal te onderzoeken machines
  per insertion een goede balans tussen oplossingskwaliteit en rekentijd?
'''