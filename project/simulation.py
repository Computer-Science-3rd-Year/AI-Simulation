import itertools
import random
import simpy
import simpy.resources
import simpy.resources.resource
import hotel
from tourists import execute_action
from tourists import beliefs, desires


###############
#DATA
###############
""" SIMULATION """
RANDOM_SEED = 42
T_INTER = [30, 300]            # intervalo entre la llegada de los turistas
SIM_TIME = 1000              # tiempo total de la simulación

""" ROOM """
ROOM_CLEANING_SIZE = 200       # máximo nive de limpieza de una habitación 
THRESHOLD_CLEAN = 80           # mínimo de limpieza/confort (% del total)

""" POOL """
POOL_CLEANING_SIZE = 100       # máximo nive de limpieza de una habitación 
THRESHOLD_CLEAN = 50           # mínimo de limpieza/confort (% del total)

""" TOURIST """
TOURIST_ENERGY_SIZE = 100        # nivel máximo de descanso
TOURIST_ENERGY_LEVEL = [20, 50]  # nivel inicial de energía de los turistas (menor_energía => más_sueño)
TOURIST_HUNGER_SIZE = 100        # nivel máximo de llenura por comida
TOURIST_HUNGER_LEVEL = [20, 50]  # nivel inicial de hambre de los turistas (menor_nivel => más_hambre)
TOURIST_FUN_SIZE = 100           # nivel máximo de diversión
TOURIST_FUN_LEVEL = [20, 50]     # nivel inicial de diversión de los turistas
TOURIST_COMFORT_SIZE = 100       # nivel máximo de confort
TOURIST_COMFORT_LEVEL = [20, 50] # nivel inicial de confort de los turistas (menor_energía => más_sueño)

TOURIST_ROOMS = {}

LEN_OF_STAY = [100, 200]
SLEEP_SPEED = 2                  # velocidad de recuperar energía (u / second)

""" WORKER """
HOUSEMAID_TIME = 50           # tiempo que tarda la mucama en limpiar la habitación (segundos)


""" MONEY """
PRICES = {}
PRICES['room'] = 50
PRICES['pool'] = 10
PRICES['buffet'] = 20
PRICES['bar'] = 30

SALARIES = {}
SALARIES['housemaid'] = 5

SALARIES_AMOUNT = {}             # salario cobrado por cada trabajador
SALARIES_AMOUNT['housemaid'] = 0

AMOUNT = {}                    # pago acumulado por Los turistas en cada servicio
AMOUNT['room'] = 0
AMOUNT['pool'] = 0
AMOUNT['buffet'] = 0
AMOUNT['bar'] = 0

def rule_of_three(numerator, denominator, factor):
    return (numerator/denominator)*factor


#Red Social
SATISFACTION = {} # ['tourist_name'] = {['necesity'] = level_when_leaves_the_hotel}

###############################################################################
#AGENT Tourist
###############################################################################

def tourist_(env, hotel, name_, beliefs, desires, type_, len_of_stay):
    perception = {}
    NECESITY_SIZE = 100
    NUMBER = 10
    print(beliefs)
    def brf(hotel):
        if type_ == 'tourist':
            for service in hotel.services:
                #necesity = service.necesity
                #name = service.name
                #if not necesity in perception and hotel.services[service]:
                #    perception[necesity] = {name}
                #    continue
                #if necesity in perception and not name in perception[necesity] and hotel.services[service]:
                #    perception[necesity].update([name])
                #    continue                
                #if name in perception[necesity] and not hotel.services[service]:
                #    perception[necesity].remouve(name)         
                if not service in perception and hotel.services[service]:
                    perception[service] = True
                if service in perception and not hotel.services[service]:
                    del perception[service]
    
    def generate_option():
        if not beliefs['has_room']:
            desires['want_room'] = True
            return
        if beliefs['energy_level'][0] < 50:
            desires['want_energy'] = True
            return
        if beliefs['food_level'][0] < 60:
            desires['want_food'] = True
            return
        if beliefs['fun_level'][0] < 40:
            desires['want_fun'] = True
            return
        else:
            desires['want_fun'] = True

    def filter():
        #print(desires)
        if desires['want_room']:
            intentions = ('reserve_room', 'energy')
            
        if desires['want_energy']:
            intentions = (random.choice(list(set(beliefs['energy_level'][1]).intersection(perception_filter(perception, 'energy')))), 'energy')
            
        if desires['want_food']:
            intentions = (random.choice(list(set(beliefs['food_level'][1]).intersection(perception_filter(perception, 'food')))), 'food')
        
        if desires['want_fun']:
            intentions = (random.choice(list(set(beliefs['fun_level'][1]).intersection(perception_filter(perception, 'fun')))), 'fun')  
        
        return intentions
    
    def perception_filter(perception, necesity): 
        available_services = []        
        for p in perception:
            if p.necesity == necesity:
                available_services.append(p.name)
        return set(available_services)
        
    
    def execute_action_(intention, hotel):
        
        if intention[0] == 'reserve_room':
            for room in hotel.rooms.services:
                if room.resource.count == 0:
                    with room.resource.request() as request_room:
                        yield request_room
                        beliefs['has_room'] = True
                        beliefs['my_room'] = room

                        desires['want_room'] = False                            
                        print(f'El turista {name_} accedió a la habitación {room.name}.')
                        print(f'LEVEL OF CLEAN OF {room.name}: {room.utilities.container.level}')
                        
                        yield hotel.env.timeout(200)
                        break  # Salir del bucle una vez que se reserve una habitación

        elif intention[0] == 'rest_room':
            my_room = beliefs['my_room']
            if my_room:
                necesity_level = intention[1] + '_level'
                cant_required = max(NECESITY_SIZE - beliefs[necesity_level][0], 1)

                with my_room.resource.request() as request_service:
                    yield request_service
                    if my_room.utilities.container.level >= cant_required and cant_required != 1:
                        my_room.utilities.container.get(cant_required)
                        print(f'El turista {name_} accedió al servicio {my_room.name}.', beliefs[necesity_level][0])
                        beliefs[necesity_level][0] += cant_required
                        desires['want_' + intention[1]] = False
                        print(beliefs[necesity_level][0])
                        
                        yield hotel.env.timeout(NUMBER)
                    elif cant_required == 1:
                        print(f'Habitación {my_room.name} con CLEAN LEVEL = {my_room.utilities.container.level}\n y {name_} necesita {NECESITY_SIZE - beliefs[necesity_level][0]} de energy')

        else:            
            for service in hotel.services:
                if service.name == intention[0]:
                    necesity_level = intention[1] + '_level'
                    cant_required = max(NECESITY_SIZE - beliefs[necesity_level][0], 1)
    
                    with service.resource.request() as request_service:
                        yield request_service
                        if service.utilities[0].container.level >= cant_required:
                            service.utilities[0].container.get(cant_required)
                            print(f'El turista {name_} accedió al servicio {service.name}.', beliefs[necesity_level][0])
                            beliefs[necesity_level][0] += cant_required
                            desires['want_' + intention[1]] = False
                            print(beliefs[necesity_level][0])
                            yield hotel.env.timeout(random.randint(1,30))
                            
                
    def action(hotel, env):
        brf(hotel)
        generate_option()
        intentions = filter()
        env.process(execute_action_(intentions, hotel))
        return intentions 
    

    now = env.now
    while env.now < now + len_of_stay:
        action(hotel, env)
        
        yield env.timeout(random.randint(1, 3))  # Tiempo de espera

###################################################
#AGENT Workers
###################################################

def housemaid(env, room):
    """Arrives at the room and finish of clean it after a certain delay."""
    #add si no tiene el salario completo no rellena al máximo el nivel de limpieza
    yield env.timeout(2)

    with room.resource.request() as rq:
        yield rq
        print(f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities.name} of the {room.name}...')
        bed = room.utilities.container
        amount = bed.capacity - bed.level
        print(f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}')
        bed.put(amount)
        yield env.timeout(HOUSEMAID_TIME)

    print(
        f'{env.now:6.1f} s: Housemaid finished and the room is clean'
    )
    print(f'Level after clean {room.name}: {bed.level}')

def interviewer(env):
    pass

def receptionist(env):
    pass

def bartender(env):
    pass

def pool_cleaner(env):
    pass

#######################################################################################
#AGENT Manager
#######################################################################################

def manager(env, rooms):
    """Periodically check the clean level of the room and call the housemaid
       if the level falls below a threshold."""
    while True:
        # DO SOMETHING FOR VERIFY THE EVOLUTION OF THE AMOUNT%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$###################
        # 

        
        # actual_amount = AMOUNT
        # yield env.timeout(30)
        # diff = DeepDiff(actual_amount, AMOUNT)
        # print(f'Actualization of evolution of amount: {diff}')

        for room in rooms:

            if room.utilities.container.level / room.utilities.container.capacity * 100 < THRESHOLD_CLEAN:
                # We need to call the housemaid now!
                
                # Wait for the housemaid to clean the room
                yield env.process(housemaid(env, room))

                housemaid_salary = SALARIES['housemaid']

                if AMOUNT['room'] >= housemaid_salary:
                    AMOUNT['room'] -= housemaid_salary
                    SALARIES_AMOUNT['housemaid'] += housemaid_salary
                    #print(f'{env.now:6.1f} s: The housemaid charaged ${housemaid_salary}. The amount salary of housemaid is {SALARIES_AMOUNT['housemaid']}')

                # else: (algo con el rendimiento de la housemaid al limpiar la habitación)
        
        yield env.timeout(5)  # Check every 5 seconds

        # añadir análisis con las ganancias

    
def tourist_generator(env, hotel):
    """Generate new tourists that arrive at the hotel."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(tourist_(env, hotel, 'tourist' + str(i), beliefs(), desires(), 'tourist', 20))

# Setup and start the simulation
print('Hotel is open')
#random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()  # hotel

#initial services
rest_room = hotel.Service(simpy.Resource(env, capacity = 10), 'rest_room', 'energy', [hotel.Utility('bed', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
pool = hotel.Service(simpy.Resource(env, capacity=11), 'pool', 'fun', [hotel.Utility('pool_utl', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
coffee = hotel.Service(simpy.Resource(env, capacity=4), 'coffee', 'energy', [hotel.Utility('bar_utl', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
energy_drink = hotel.Service(simpy.Resource(env, capacity=4), 'energy_drink', 'energy', [hotel.Utility('bar_utl', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
buffet = hotel.Service(simpy.Resource(env, capacity = 10), 'buffet', 'food', [hotel.Utility('buffet', simpy.Container(env, ROOM_CLEANING_SIZE, init= ROOM_CLEANING_SIZE))])
snack_bar = hotel.Service(simpy.Resource(env, capacity = 7), 'snack_bar', 'food', [hotel.Utility('snack_bar', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
room_service = hotel.Service(simpy.Resource(env, capacity = 11), 'room_service', 'food', [hotel.Utility('room_service', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
restaurant = hotel.Service(simpy.Resource(env, capacity = 7), 'restaurant', 'food', [hotel.Utility('restaurant', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
ranchon = hotel.Service(simpy.Resource(env, capacity = 5), 'ranchon', 'food', [hotel.Utility('ranchon', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
pool_table = hotel.Service(simpy.Resource(env, capacity = 2), 'pool_table', 'fun', [hotel.Utility('pool_table', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
table_tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'table_tennis', 'fun', [hotel.Utility('table_tennis', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'tennis', 'fun', [hotel.Utility('tennis', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
gym = hotel.Service(simpy.Resource(env, capacity = 11), 'gym', 'fun', [hotel.Utility('gym', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
show_time = hotel.Service(simpy.Resource(env, capacity = 11), 'show_time', 'fun', [hotel.Utility('show_time', simpy.Container(env, ROOM_CLEANING_SIZE, init=ROOM_CLEANING_SIZE))])
services = [rest_room, pool, coffee, energy_drink, buffet, snack_bar, room_service, restaurant, ranchon, pool_table, table_tennis, 
            tennis, gym, show_time]

melia_hotel = hotel.Hotel(services, env)

env.process(manager(env, melia_hotel.rooms.services))
env.process(tourist_generator(env, melia_hotel))

# Execute!
env.run(until=SIM_TIME)
