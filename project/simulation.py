import itertools
import random
import simpy
import hotel
import params as prm
import tourists as t

outputs = []

#Red Social
SATISFACTION = {} # ['tourist_name'] = {['necesity'] = level_when_leaves_the_hotel}

###############################################################################
#-------------------------T   O   U   R   I   S   T----------------------------
###############################################################################

def tourist_(env, hotel, name, beliefs, desires, len_of_stay, arrive_time):
    perception = {}
    outputs.append((env.now, beliefs))
    
    def execute_action_(intentions, hotel):
        for intention in intentions:
            if intention[0] == 'reserve_room':
                beliefs['using_service'] = True
                for room in hotel.rooms.services:
                    if room.resource.count == 0:
                        with room.resource.request() as request_room:
                            yield request_room
                            beliefs['has_room'] = True
                            beliefs['my_room'] = room
                            desires['want_room'] = False  
                            outputs.append((env.now,f'El turista {name} accedió a la habitación {room.name}.')) 
                            outputs.append((env.now,f'LEVEL OF CLEAN OF {room.name}: {room.utilities.container.level}'))                            
                            yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                            beliefs['using_service'] = False
                            break

            elif intention[0] == 'rest_room':
                beliefs['using_service'] = True
                my_room = beliefs['my_room']
                if my_room:
                    necesity_level = intention[1] + '_level'
                    cant_required = prm.NECESITY_SIZE - beliefs[necesity_level][0]
                    if cant_required > 0:
                        with my_room.resource.request() as request_service:
                            yield request_service
                            if my_room.utilities.container.level >= cant_required and cant_required != 1:
                                my_room.utilities.container.get(cant_required)
                                outputs.append((env.now, f'El turista {name} accedió al servicio {my_room.name}, {beliefs[necesity_level][0]}'))
                                beliefs[necesity_level][0] += cant_required
                                desires['want_' + intention[1]] = False
                                outputs.append((env.now,beliefs[necesity_level][0]))
                                yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                                beliefs['using_service'] = False

                            else:
                                beliefs['using_service'] = False
                                outputs.append((env.now, f'Habitación {my_room.name} con CLEAN LEVEL = {my_room.utilities.container.level}\n y {name} necesita {prm.NECESITY_SIZE - beliefs[necesity_level][0]} de energy'))
                    else:
                        with my_room.resource.request() as request_service:
                            yield request_service
                            outputs.append((env.now, f'El turista {name} accedió al servicio {my_room.name}, {beliefs[necesity_level][0]}'))
                            desires['want_' + intention[1]] = False
                            outputs.append((env.now,beliefs[necesity_level][0]))
                            yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                            beliefs['using_service'] = False
            else:            
                for service in hotel.services:
                    if service.name == intention[0]:
                        beliefs['using_service'] = True
                        necesity_level = intention[1] + '_level'
                        cant_required = prm.NECESITY_SIZE - beliefs[necesity_level][0]
                        if cant_required > 0:        
                            with service.resource.request() as request_service:
                                yield request_service
                                if service.utilities[0].container.level >= cant_required:
                                    service.utilities[0].container.get(cant_required)
                                    outputs.append((env.now, f'El turista {name} accedió al servicio {service.name}, {beliefs[necesity_level][0]}'))
                                    beliefs[necesity_level][0] += cant_required
                                    desires['want_' + intention[1]] = False
                                    outputs.append((env.now,beliefs[necesity_level][0]))
                                    yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                                    beliefs['using_service'] = False
                                else:
                                    beliefs['using_service'] = False
                                    outputs.append((env.now, f'The service {service.name} con CLEAN LEVEL = {service.utilities.container.level}\n y {name} necesita {prm.NECESITY_SIZE - beliefs[necesity_level][0]} de {intention[1]}'))
                        else:
                            with service.resource.request() as request_service:
                                yield request_service
                                outputs.append((env.now, f'El turista {name} accedió al servicio {service.name}, {beliefs[necesity_level][0]}'))
                                desires['want_' + intention[1]] = False
                                outputs.append((env.now,beliefs[necesity_level][0]))
                                yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                                beliefs['using_service'] = False  
                            
                
    def action(hotel):
        t.brf(hotel, perception)
        t.generate_option(beliefs, desires)
        intentions = t.filter(beliefs, desires, perception)
        return intentions 
    
    while env.now < arrive_time + len_of_stay:
        intentions = action(hotel)        
        while beliefs['using_service']:
            yield env.timeout(1)
        env.process(execute_action_(intentions, hotel))
        yield env.timeout(random.randint(1, 3))  # Tiempo de espera
        if env.now >= arrive_time + len_of_stay:
            outputs.append((env.now, f'{name} left the hotel at {env.now}\narrive: {arrive_time}\nlen of stay: {len_of_stay}'))
            break
        outputs.append((env.now, 'aaaaaaaaaaaaaaaaa!!!!!!!!!!'))
    
    

###############################################################################
#------------------------- W   O   R   K   E   R   S --------------------------
###############################################################################

def housemaid(env, room):
    """Arrives at the room and finish of clean it after a certain delay."""
    #add si no tiene el salario completo no rellena al máximo el nivel de limpieza
    yield env.timeout(2)

    with room.resource.request() as rq:
        yield rq
        outputs.append((env.now, f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities.name} of the {room.name}...'))
        #print(f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities.name} of the {room.name}...')-----------------------------
        bed = room.utilities.container
        amount = bed.capacity - bed.level
        outputs.append((env.now, f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}'))
        #print(f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}')---------------------------------------
        bed.put(amount)
        yield env.timeout(prm.HOUSEMAID_TIME)

    outputs.append((env.now, f'{env.now:6.1f} s: Housemaid finished and the room is clean'))
    outputs.append((env.now, f'Level after clean {room.name}: {bed.level}'))
    #print(f'{env.now:6.1f} s: Housemaid finished and the room is clean')---------------------------------------------
    #print(f'Level after clean {room.name}: {bed.level}')-----------------------------------------------------

def interviewer(env):
    pass

def receptionist(env):
    pass

def bartender(env):
    pass

def pool_cleaner(env):
    pass

###############################################################################
#------------------------- M   A   N   A   G   E   R --------------------------
###############################################################################

def manager(env, rooms):
    """Periodically check the clean level of the room and call the housemaid
       if the level falls below a threshold."""
    while True:
        # DO SOMETHING FOR VERIFY THE EVOLUTION OF THE AMOUNT%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$###################
        
        # actual_amount = AMOUNT
        # yield env.timeout(30)
        # diff = DeepDiff(actual_amount, AMOUNT)
        # print(f'Actualization of evolution of amount: {diff}')

        for room in rooms:

            if room.utilities.container.level / room.utilities.container.capacity * 100 < prm.THRESHOLD_CLEAN:
                # We need to call the housemaid now!
                
                # Wait for the housemaid to clean the room
                yield env.process(housemaid(env, room))

                housemaid_salary = prm.SALARIES['housemaid']

                if prm.AMOUNT['room'] >= housemaid_salary:
                    prm.AMOUNT['room'] -= housemaid_salary
                    prm.SALARIES_AMOUNT['housemaid'] += housemaid_salary
                    #print(f'{env.now:6.1f} s: The housemaid charaged ${housemaid_salary}. The amount salary of housemaid is {SALARIES_AMOUNT['housemaid']}')

                # else: (algo con el rendimiento de la housemaid al limpiar la habitación)
        
        yield env.timeout(5)  # Check every 5 seconds

        # añadir análisis con las ganancias

    
def tourist_generator(env, hotel):
    """Generate new tourists that arrive at the hotel."""
    for i in itertools.count():
        yield env.timeout(random.randint(*prm.T_INTER))
        len_of_stay = random.randint(*prm.LEN_OF_STAY)
        env.process(tourist_(env, hotel, f'Tourist_{i}', t.beliefs(), t.desires(), len_of_stay, env.now))



###########################################################################################
#--------------------------- S      T      A      R      T --------------------------------
###########################################################################################

# Create environment and start processes
env = simpy.Environment()  # hotel
outputs.append((env.now, 'Hotel is open'))

# energy = enu.Necesity.energy.name
# food = enu.Necesity.food.name
# fun = enu.Necesity.fun.name

#initial services
rest_room = hotel.Service(simpy.Resource(env, capacity = 10), 'rest_room', prm.energy, [hotel.Utility('bed', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
pool = hotel.Service(simpy.Resource(env, capacity=11), 'pool', prm.fun, [hotel.Utility('pool_utl', simpy.Container(env, prm.POOL_CLEANING_SIZE, init=prm.POOL_CLEANING_SIZE))])
coffee = hotel.Service(simpy.Resource(env, capacity=4), 'coffee', prm.energy, [hotel.Utility('bar_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
energy_drink = hotel.Service(simpy.Resource(env, capacity=4), 'energy_drink', prm.energy, [hotel.Utility('bar_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
buffet = hotel.Service(simpy.Resource(env, capacity = 10), 'buffet', prm.food, [hotel.Utility('buffet', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))])
snack_bar = hotel.Service(simpy.Resource(env, capacity = 7), 'snack_bar', prm.food, [hotel.Utility('snack_bar', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
room_service = hotel.Service(simpy.Resource(env, capacity = 11), 'room_service', prm.food, [hotel.Utility('room_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
restaurant = hotel.Service(simpy.Resource(env, capacity = 7), 'restaurant', prm.food, [hotel.Utility('restaurant', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
ranchon = hotel.Service(simpy.Resource(env, capacity = 5), 'ranchon', prm.food, [hotel.Utility('ranchon', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
pool_table = hotel.Service(simpy.Resource(env, capacity = 2), 'pool_table', prm.fun, [hotel.Utility('pool_table', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
table_tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'table_tennis', prm.fun, [hotel.Utility('table_tennis', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'tennis', prm.fun, [hotel.Utility('tennis', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
gym = hotel.Service(simpy.Resource(env, capacity = 11), 'gym', prm.fun, [hotel.Utility('gym', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
show_time = hotel.Service(simpy.Resource(env, capacity = 11), 'show_time', prm.fun, [hotel.Utility('show_time', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))])
services = [rest_room, pool, coffee, energy_drink, buffet, snack_bar, room_service, restaurant, ranchon, pool_table, table_tennis, 
            tennis, gym, show_time]

melia_hotel = hotel.Hotel(services, env)

env.process(manager(env, melia_hotel.rooms.services))
env.process(tourist_generator(env, melia_hotel))

# Execute!
env.run(until=prm.SIM_TIME)
for timestamp, mensaje in sorted(outputs, key = lambda outputs_: outputs_[0]):
        print(f"{timestamp}: {mensaje}")
