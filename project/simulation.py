import itertools
import random
import simpy
import os
import scipy.stats as stats
import hotel
import params as prm
import tourists as t
import housemaid as hsd
import manager as mg
import receptionist as recp
from hotel_services import create_services, basic_services
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
        if beliefs['my_room'] == 1:
            return
        yield env.timeout(random.randint(1, 3))  # Tiempo de espera
        
        #print(f'{name} left the hotel at {env.now}\narrive: {arrive_time}\nlen of stay: {len_of_stay}')
    outputs.append((env.now, f'{name} left the hotel at {env.now}\narrive: {arrive_time}\nlen of stay: {len_of_stay}'))
    experience_ = ""
    for sentence in experience:
        experience_+=sentence
    EXPERIENCES[f'{name}'] = experience_
    #print(f'{name}: {experience_}')
    beliefs['my_room'] = None
    #outputs.append((env.now, 'aaaaaaaaaaaaaaaaa!!!!!!!!!!'))

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
            ##print('room', dict[item[0]])
            item[1]['my_room'] = dict[item[0]]
            if dict[item[0]] != None:
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

def manager(env, rooms, hotel, services_, test):

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
                #print('NULL INTENTIOONNNNSSSS############')
                yield env.timeout(40)
                continue

            #print(intentions)
        env.process(mg.execute_action(env, intentions, hotel, services_, outputs, beliefs, desires, test))
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
env = simpy.Environment()
services_ = create_services(env)
outputs.append((env.now, 'Hotel is open'))

services = basic_services(env)
melia_hotel = hotel.Hotel(services, env)

env.process(manager(env, melia_hotel.rooms.services, melia_hotel, services_, True))
env.process(tourist_generator(env, melia_hotel))
env.process(receptionist(env, melia_hotel))

# Execute!
env.run(until=prm.SIM_TIME)
# NO BORRARRR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#print(EXPERIENCES)
#for tourist in EXPERIENCES:
#    review = llm.generate_review(EXPERIENCES[tourist])
#    classif = llm.classify_review(review)
#    outputs.append(f'{tourist}:\n{review}\nCLASSIFICATION --> {classif}\n')
#    print(f'{tourist}:\n{review}\nCLASSIFICATION --> {classif}\n') 
#    #print(f'{tourist}: {experience}\n')
os.remove("output.txt")
with open("output.txt", "a") as f:
    for timestamp, message in sorted(outputs, key = lambda outputs_: outputs_[0]):
            f.write(f"{timestamp}: {message}" + '\n')
##################################################################################
def best_strategy(test):
    result = []
    global reserved
    global reserved_bool
    global reserved_time
    global EXPERIENCES
    global REVIEWS
    global CLASSIFICATION
    for i in range(100):

        prm.HOUSEMAID_TIME = 15
        prm.REPAIRMAN_TIME = 40
        reserved = [] # [(tourist_name, tourist_beliefs, len_of_stay), ...]
        reserved_bool = [] # [tourist_1, tourist_2, ...] turistas que se han hospedado en el hotel
        reserved_time = {} # {'tourist_1': check-out time, 'tourist_2': check-out time,...}
        #Red Social
        EXPERIENCES = {} # {'tourist_name': experience}
        REVIEWS = {} # {'tourist_name': review}
        CLASSIFICATION = {} 
        env = simpy.Environment()
        services = basic_services(env)
        melia_hotel = hotel.Hotel(services, env)
        services_ = create_services(env)
        env.process(manager(env, melia_hotel.rooms.services, melia_hotel, services_, test))
        env.process(tourist_generator(env, melia_hotel))
        env.process(receptionist(env, melia_hotel))

        env.run(until=prm.SIM_TIME)
        result.append(melia_hotel.budget)

    return result

estrategy_for_limit = best_strategy(True)
estrategy_for_iter = best_strategy(False)

# Prueba de Mann-Whitney U
u_statistic, p_value = stats.mannwhitneyu(estrategy_for_limit, estrategy_for_iter)

print("\nPrueba de Mann-Whitney U:")
print("Estadístico U:", u_statistic)  # Mide la diferencia en los rangos de los datos
print("Valor p:", p_value)  # Probabilidad de obtener los resultados observados si no hay diferencia real

# Interpretación de los resultados:
alpha = 0.05  # Nivel de significancia

if p_value < alpha:
    print("\nExiste una diferencia significativa en la ganancia entre las estrategias.")
    print("Se rechaza la hipótesis nula de que no hay diferencia.")
    print("Podemos concluir que la estrategia que produjo los datos con mayor media es mejor.")
else:
    print("\nNo se encontró una diferencia significativa en la ganancia entre las estrategias.")
    print("Se acepta la hipótesis nula de que no hay diferencia.")
    print("No podemos concluir que una estrategia sea mejor que la otra.")