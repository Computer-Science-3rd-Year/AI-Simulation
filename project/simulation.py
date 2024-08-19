import itertools
import random
import simpy
import copy
import hotel
import params as prm
import enums as enu
import tourists as t
import housemaid as hsd
import generic_worker as gw
import manager as mg
import receptionist as recp
from hotel_services import env, services_
import llm

outputs = []
reserved = [] # [(tourist_name, tourist_beliefs, len_of_stay), ...]
reserved_bool = [] # [tourist_1, tourist_2, ...] turistas que se han hospedado en el hotel
reserved_time = {} # {'tourist_1': check-out time, 'tourist_2': check-out time,...}
#Red Social
EXPERIENCES = {} # {'tourist_name': experience}
REVIEWS = {} # {'tourist_name': review}
CLASSIFICATION = {} # {'tourist_name': calssifications of review}
###############################################################################
#-------------------------T   O   U   R   I   S   T----------------------------
###############################################################################

def tourist_(env, hotel, name, beliefs, desires, len_of_stay, arrive_time):
    perception = {
        prm.energy: [],
        prm.food: [],
        prm.fun: [],
        prm.comfort: []
    }
    experience = []
    global reserved 
    #outputs.append((env.now, beliefs))
    
    while env.now < arrive_time + len_of_stay:
        t.communicate(env, reserved, reserved_time, beliefs)            
        t.brf(hotel, perception, beliefs)
        t.generate_option(beliefs, desires, env)
        intentions = t.filter(beliefs, desires, perception)

        if not intentions:
            yield env.timeout(10)
            continue       
        while beliefs['using_service']:
            yield env.timeout(1)
        env.process(t.execute_action_(intentions, hotel, experience, name, reserved, outputs, len_of_stay, env, beliefs, desires))
        yield env.timeout(random.randint(1, 3))  # Tiempo de espera

        if env.now >= arrive_time + len_of_stay:
            beliefs['my_room'] = None
            outputs.append((env.now, f'{name} left the hotel at {env.now}\narrive: {arrive_time}\nlen of stay: {len_of_stay}'))
            experience_ = ""
            for sentence in experience:
                experience_+=sentence
            EXPERIENCES[f'{name}'] = experience_
            # review = llm.generate_review(experience_)
            # classif = llm.classify_review(review)
            # REVIEWS[f'{name}'] = review
            # CLASSIFICATION[f'{name}'] = classif
            break
        outputs.append((env.now, 'aaaaaaaaaaaaaaaaa!!!!!!!!!!'))

###############################################################################
#------------------------- W   O   R   K   E   R   S --------------------------
###############################################################################

def housemaid(env, rooms, hotel):
    """Arrives at the room and finish of clean it after a certain delay."""
    #add si no tiene el salario completo no rellena al máximo el nivel de limpieza
    beliefs = hsd.beliefs(rooms)
    desires = hsd.desires(beliefs)

    hsd.execute_action(env, rooms, hotel, beliefs, outputs)
    
    time = env.now
    while time <  prm.SIM_TIME:
        while beliefs['working']:
            yield env.timeout(1)

        hsd.brf(hotel, beliefs)
        hsd.generate_option(beliefs, desires)
        intentions = hsd.filter(desires)        
        env.process(hsd.execute_action(env, intentions, hotel, beliefs, outputs))
        time = env.now
        yield env.timeout(5)
    
def receptionist(env, hotel):
    time = env.now
    while time < prm.SIM_TIME:

        reserved_ = []
        for item in reserved:
            if item[0] in reserved_bool:
                continue
            reserved_.append(item)
            
        ordenated_tourist = sorted(reserved_, key= lambda tupla: len(tupla[1]['restrictions']))
        dict = recp.rooms_distributions(ordenated_tourist, 0, {}, time, hotel, reserved_time)
       
        recp.bad_room(dict, hotel, time, ordenated_tourist, reserved_time)
        for item in ordenated_tourist:
            print('room', dict[item[0]])
            item[1]['my_room'] = dict[item[0]]
            hotel.revenues[dict[item[0]]] += dict[item[0]].price
            hotel.budget += dict[item[0]].price
            outputs.append((env.now,f'El turista {item[0]} accedió a la habitación {dict[item[0]].name}.')) 
            outputs.append((env.now,f'LEVEL OF CLEAN OF {dict[item[0]].name}: {dict[item[0]].utilities[0].container.level}'))
            reserved_time[dict[item[0]]] = env.now + item[2]
            reserved_bool.append(item[0])
        yield env.timeout(70)
        time = env.now

###############################################################################
#------------------------- M   A   N   A   G   E   R --------------------------
###############################################################################

def manager(env, rooms, hotel):

    beliefs = mg.beliefs(hotel)
    desires = mg.desires()

    #Asignar las habitaciones respectivas a cada housemaid
    rooms_housemaid = []
    count = 0
    for room in rooms:
        rooms_housemaid.append(room)
        count += 1
        if count == 2:
            housemaid_ = env.process(housemaid(env, rooms_housemaid, hotel))
            room.worker = housemaid_
            count = 0
            salary = random.randint(*prm.SALARIES)
            for room1 in rooms_housemaid:
                room1.worker = [housemaid_, salary]
            rooms_housemaid = []
            yield env.timeout(1)

    for service in hotel.services:
        worker = env.process(mg.generic_worker(env, service.name+'_worker', service, hotel, outputs))
        service.worker = [worker, random.randint(*prm.SALARIES)]
        yield env.timeout(1)
    
    time = env.now
    while time <  prm.SIM_TIME:
        if env.now >= prm.SIM_TIME/5: beliefs['wait'] = False

        if time - hotel.peak_season_time > prm.SEASON_TIME:
            hotel.peak_season = not hotel.peak_season
            hotel.peak_season_time = time

        while beliefs['working']:
            yield env.timeout(1)
                
        if beliefs['wait']: return
        mg.brf()
        mg.generate_options(beliefs, desires, env, hotel)
        intentions = mg.filter(beliefs, desires)

        if not intentions:
            if beliefs['nothing']: beliefs['nothing'] = False
            if not beliefs['wait']:
                print('NULL INTENTIOONNNNSSSS############')
                yield env.timeout(40)
                continue

            #print(intentions)
        env.process(mg.execute_action(env, intentions, hotel, services_, outputs, beliefs, desires))
        time = env.now
        yield env.timeout(40)

###########################################################################################
#--------------------------- S      T      A      R      T --------------------------------
###########################################################################################
def tourist_generator(env, hotel):
    """Generate new tourists that arrive at the hotel."""
    for i in itertools.count():
        yield env.timeout(random.randint(*prm.T_INTER))
        len_of_stay = random.randint(*prm.LEN_OF_STAY)
        env.process(tourist_(env, hotel, f'Tourist_{i}', t.beliefs(hotel), t.desires(), len_of_stay, env.now))

outputs.append((env.now, 'Hotel is open'))

#initial services
rest_room = hotel.Service(simpy.Resource(env, capacity = 10), 'rest_room', prm.energy, [hotel.Utility('bed', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.ROOM_PRICE)
pool = hotel.Service(simpy.Resource(env, capacity=11), 'pool', prm.fun, [hotel.Utility('pool_utl', simpy.Container(env, prm.POOL_CLEANING_SIZE, init=prm.POOL_CLEANING_SIZE))], prm.POOL_PRICE)
coffee = hotel.Service(simpy.Resource(env, capacity=4), 'coffee', prm.energy, [hotel.Utility('bar_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.COFFEE_PRICE)
energy_drink = hotel.Service(simpy.Resource(env, capacity=4), 'energy_drink', prm.energy, [hotel.Utility('bar_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.ENERGY_DRINK_PRICE)
buffet = hotel.Service(simpy.Resource(env, capacity = 10), 'buffet', prm.food, [hotel.Utility('buffet', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], prm.BUFFET_PRICE)
snack_bar = hotel.Service(simpy.Resource(env, capacity = 7), 'snack_bar', prm.food, [hotel.Utility('snack_bar', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.SNACK_BAR_PRICE)
room_service = hotel.Service(simpy.Resource(env, capacity = 11), 'room_service', prm.food, [hotel.Utility('room_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.ROOM_SERVICE_PRICE)
restaurant = hotel.Service(simpy.Resource(env, capacity = 7), 'restaurant', prm.food, [hotel.Utility('restaurant', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.RESTAURANT_PRICE)
ranchon = hotel.Service(simpy.Resource(env, capacity = 5), 'ranchon', prm.food, [hotel.Utility('ranchon', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.RANCHON_PRICE)
pool_table = hotel.Service(simpy.Resource(env, capacity = 2), 'pool_table', prm.fun, [hotel.Utility('pool_table', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.POOL_TABLE_PRICE)
table_tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'table_tennis', prm.fun, [hotel.Utility('table_tennis', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.TABLE_TENNIS_PRICE)
tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'tennis', prm.fun, [hotel.Utility('tennis', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.TENNIS_PRICE)
gym = hotel.Service(simpy.Resource(env, capacity = 11), 'gym', prm.fun, [hotel.Utility('gym', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.GYM_PRICE)
show_time = hotel.Service(simpy.Resource(env, capacity = 11), 'show_time', prm.fun, [hotel.Utility('show_time', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.SHOW_TIME_PRICE)
services = [rest_room, pool, coffee, energy_drink, buffet, snack_bar, room_service, restaurant, ranchon, pool_table, table_tennis, 
            tennis, gym, show_time]

melia_hotel = hotel.Hotel(services, env)

env.process(manager(env, melia_hotel.rooms.services, melia_hotel))
env.process(tourist_generator(env, melia_hotel))
env.process(receptionist(env, melia_hotel))

# Execute!
env.run(until=prm.SIM_TIME)
for timestamp, message in sorted(outputs, key = lambda outputs_: outputs_[0]):
        print(f"{timestamp}: {message}")

# NO BORRARRR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# for tourist in EXPERIENCES:
#     review = llm.generate_review(EXPERIENCES[tourist])
#     classif = llm.classify_review(review)
#     print(f'{tourist}:\n{review}CLASSIFICATION --> {classif}') 
