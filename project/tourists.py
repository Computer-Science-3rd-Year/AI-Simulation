import random
import params as prm

services = {prm.energy: {prm.rest_room, prm.coffee, prm.energy_drink},
            prm.food: {prm.buffet, prm.snack_bar, prm.room_service, prm.restaurant, prm.ranchon},
            prm.fun: {prm.pool, prm.pool_table, prm.table_tennis, prm.tennis, prm.gym, prm.show_time}
            }


# servicios que un turista en particular necesita para satisfacer sus necesidades
def beliefs():
    return {
            'energy_level': [random.randint(*prm.TOURIST_ENERGY_LEVEL), random.sample(list(services[prm.energy]), random.randint(1, len(services[prm.energy])))],
            'food_level':   [random.randint(*prm.TOURIST_FOOD_LEVEL), random.sample(list(services[prm.food]), random.randint(1, len(services[prm.food])))],
            'fun_level':    [random.randint(*prm.TOURIST_FUN_LEVEL), random.sample(list(services[prm.fun]), random.randint(1, len(services[prm.fun])))],
            #'comfort_level': 
            'has_room': False,
            'my_room': None,
            'room_cleanliness': None,
            'using_service': False,
            }

def desires():
    return {
            'want_energy': False,
            'want_food': False,
            'want_fun': False,
            #'want_comfort': False,
            'want_room': False,
            }

def brf(hotel, perception):
    for service in hotel.services:
        s_necesity = service.necesity
        s_name = service.name
        if not s_necesity in perception and hotel.services[service]:
           perception[s_necesity] = [s_name]
        elif s_necesity in perception and not s_name in perception[s_necesity] and hotel.services[service]:
           perception[s_necesity].append(s_name)                
        elif s_name in perception[s_necesity] and not hotel.services[service]:
           perception[s_necesity].remove(s_name)

def generate_option(beliefs, desires):
    if not beliefs['has_room']:
        desires['want_room'] = True
    elif beliefs['energy_level'][0] < prm.THRESHOLD_ENERGY:
        desires['want_energy'] = True
    elif beliefs['food_level'][0] < prm.THRESHOLD_FOOD:
        desires['want_food'] = True
    elif beliefs['fun_level'][0] < prm.THRESHOLD_FUN:
        desires['want_fun'] = True
    else:
        desires['want_fun'] = True

def filter(beliefs, desires, perception):
        if desires['want_room']:
            intentions = [('reserve_room', prm.energy)]            
        if desires['want_energy']:
            intentions = [(random.choice(list(set(beliefs['energy_level'][1]).intersection(set(perception[prm.energy])))), prm.energy)]            
        if desires['want_food']:
            intentions = [(random.choice(list(set(beliefs['food_level'][1]).intersection(set(perception[prm.food])))), prm.food)]        
        if desires['want_fun']:
            intentions = [(random.choice(list(set(beliefs['fun_level'][1]).intersection(set(perception[prm.fun])))), prm.fun)]        
        return intentions

