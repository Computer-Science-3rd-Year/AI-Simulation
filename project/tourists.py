import random
import params as prm
import enums as en

services = {prm.energy: {prm.coffee, prm.rest_room, prm.energy_drink},
            #prm.energy: {prm.rest_room},
            prm.food: {prm.buffet, prm.snack_bar, prm.room_service, prm.restaurant, prm.ranchon},
            prm.fun: {prm.pool, prm.pool_table, prm.table_tennis, prm.tennis, prm.gym, prm.show_time}
            }


# servicios que un turista en particular necesita para satisfacer sus necesidades
def beliefs(hotel):
    Update_services(hotel)
    return {
            'energy_level': [random.randint(*prm.TOURIST_ENERGY_LEVEL), random.sample(list(services[prm.energy]), random.randint(1, len(services[prm.energy])))],
            'food_level':   [random.randint(*prm.TOURIST_FOOD_LEVEL), random.sample(list(services[prm.food]), random.randint(1, len(services[prm.food])))],
            'fun_level':    [random.randint(*prm.TOURIST_FUN_LEVEL), random.sample(list(services[prm.fun]), random.randint(1, len(services[prm.fun])))],
            'comfort_level': [random.randint(*prm.TOURIST_COMFORT_LEVEL), random.sample(list(services[prm.fun]), random.randint(1, len(services[prm.fun])))],
            'has_room': False,
            'my_room': None,
            'room_cleanliness': None,
            'using_service': False,
            'restrictions': random.sample(prm.ATTRIBUTES, random.randint(0, len(prm.ATTRIBUTES))),
            #----BELIEFS PARA LA ENCUESTA-----
            'room_features': None,    # alguno de los niveles que están en survey.py
            'room_clean_mainten': None,#  ''
            'general_quality': None, #  ''
            'used_services': {}, # servicios usados por el turista
            'amenities_variety': None,
            'staff_friendliness': None,
            'quality_price': None,
            'satisfaction': 0,
            'budget': random.randint(*prm.TOURIST_BUDGET)
            }

def desires():
    return {
            'want_energy': False,
            'want_food': False,
            'want_fun': False,
            'want_comfort': False,
            'want_room': False,
            'be_honest': True,
            'do_survey': True,
            }

def brf(hotel, perception, beliefs):
    for service in hotel.services:
        s_necesity = service.necesity
        s_name = service.name
        if not s_necesity in perception and hotel.services[service]:
           perception[s_necesity] = [s_name]
        elif s_necesity in perception and not s_name in perception[s_necesity] and hotel.services[service]:
           perception[s_necesity].append(s_name)                
        elif s_name in perception[s_necesity] and not hotel.services[service]:
           perception[s_necesity].remove(s_name)
    
    # bajar el nivel de las necesidades
    for necesity in en.Necesity:
        actual_level = beliefs[necesity.name + '_level'][0]
        actual_level = max(0,  actual_level - random.randint(0, 10))

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
            try:
                intentions = [(random.choice(list(set(beliefs['energy_level'][1]).intersection(set(perception[prm.energy])))), prm.energy)]
            except:
                intentions = [(find_available_service(perception, prm.energy), prm.energy)]
            if intentions[0][0] == prm.rest_room and  beliefs['my_room'].using:
                intentions = None
        if desires['want_food']:
            try:
                intentions = [(random.choice(list(set(beliefs['food_level'][1]).intersection(set(perception[prm.food])))), prm.food)]        
            except:
                intentions = [(find_available_service(perception, prm.food), prm.food)]
        if desires['want_fun']:
            try:
                intentions = [(random.choice(list(set(beliefs['fun_level'][1]).intersection(set(perception[prm.fun])))), prm.fun)]        
            except:
                intentions = [(find_available_service(perception, prm.fun), prm.fun)]
        return intentions

def find_available_service(perception, necesity):
    for service in perception[necesity]:
        return service
    

def room_clean_mainten_(beliefs):
    clean_level = 0
    for utility in beliefs['my_room'].utilities:
       clean_level += utility.container.level
        
    clean_level = clean_level/ len(beliefs['my_room'].utilities)

def claculate_satisfaction(beliefs):
    sum = 0
    necesities_count = 0
    for necesity in en.Necesity.name:
        necesities_count += 1
        sum += beliefs[necesity + '_level'][0]
    
    beliefs['satisfaction'] = sum/necesities_count

def Update_services(hotel):
    services[prm.energy] = set()
    services[prm.food] = set()
    services[prm.fun] = set()
    services[prm.comfort] = set()
    for service in hotel.services:
        if service.necesity == prm.energy:
            services[prm.energy].add(service.name)
        elif service.necesity == prm.food:
            services[prm.food].add(service.name)
        elif service.necesity == prm.comfort:
            pass
        else:
            services[prm.fun].add(service.name)