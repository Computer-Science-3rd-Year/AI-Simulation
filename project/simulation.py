import itertools
import random
import simpy
import hotel
import params as prm
import tourists as t
import housemaid as hsd
import generic_worker as gw
import manager as mg
outputs = []

#Red Social
SATISFACTION = {} # ['tourist_name'] = {['necesity'] = level_when_leaves_the_hotel}

###############################################################################
#-------------------------T   O   U   R   I   S   T----------------------------
###############################################################################

def tourist_(env, hotel, name, beliefs, desires, len_of_stay, arrive_time):
    perception = {}
    #outputs.append((env.now, beliefs))
    
    def execute_action_(intentions, hotel):
        if not intentions:
            return
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
                            hotel.revenues[room] += room.price
                            hotel.budget += room.price
                            outputs.append((env.now,f'El turista {name} accedió a la habitación {room.name}.')) 
                            outputs.append((env.now,f'LEVEL OF CLEAN OF {room.name}: {room.utilities[0].container.level}'))                            
                            yield hotel.env.timeout(len_of_stay)
                            beliefs['using_service'] = False
                            break

            elif intention[0] == 'rest_room':
                beliefs['using_service'] = True
                my_room = beliefs['my_room']
                outputs.append((env.now, f'{name}--> {my_room.name} jjjjjjjjjjjjjjjj'))
                if my_room:
                    my_room.using = True
                    necesity_level = intention[1] + '_level'
                    cant_required = prm.NECESITY_SIZE - beliefs[necesity_level][0]
                    if cant_required > 0:
                        with my_room.resource.request() as request_service:
                            yield request_service
                            if my_room.utilities[0].container.level >= cant_required and cant_required != 1:
                                
                                outputs.append((env.now, f'El turista {name} accedió al servicio {my_room.name}, {beliefs[necesity_level][0]}'))
                                beliefs[necesity_level][0] += cant_required
                                desires['want_' + intention[1]] = False
                                outputs.append((env.now,beliefs[necesity_level][0]))
                                yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                                beliefs['using_service'] = False
                                my_room.utilities[0].container.get(cant_required)
                            else:
                                beliefs['using_service'] = False
                                outputs.append((env.now, f'Habitación {my_room.name} con CLEAN LEVEL = {my_room.utilities[0].container.level}\n y {name} necesita {prm.NECESITY_SIZE - beliefs[necesity_level][0]} de energy'))
                    else:
                        with my_room.resource.request() as request_service:
                            yield request_service
                            outputs.append((env.now, f'El turista {name} accedió al servicio {my_room.name}, {beliefs[necesity_level][0]}'))
                            desires['want_' + intention[1]] = False
                            outputs.append((env.now,beliefs[necesity_level][0]))
                            yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                            beliefs['using_service'] = False
                my_room.using = False
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
                                    hotel.revenues[service] += service.price
                                    hotel.budget += service.price
                                    outputs.append((env.now,beliefs[necesity_level][0]))
                                    yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
                                    beliefs['using_service'] = False
                                else:
                                    beliefs['using_service'] = False
                                    outputs.append((env.now, f'The service {service.name} con CLEAN LEVEL = {service.utilities[0].container.level}\n y {name} necesita {prm.NECESITY_SIZE - beliefs[necesity_level][0]} de {intention[1]}'))
                        else:
                            with service.resource.request() as request_service:
                                yield request_service
                                hotel.revenues[service] += service.price
                                hotel.budget += service.price
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

def housemaid(env, rooms, hotel):
    """Arrives at the room and finish of clean it after a certain delay."""
    #add si no tiene el salario completo no rellena al máximo el nivel de limpieza
    beliefs = hsd.beliefs(rooms)
    desires = hsd.desires(beliefs)

    
    def execute_action(env, rooms, hotel):
        #print('housemaiddddddddddd')
        if rooms == []:
            return       
        for room in rooms:
            beliefs['working'] = True
            with room.resource.request() as rq: 
                room.using = True
                yield rq
                #print(f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities.name} of the {room.name}...')-----------------------------
                bed = room.utilities[0].container
                #print(bed.capacity, bed.level)
                amount = bed.capacity - bed.level
                print(f'total: {bed.capacity}, level: {bed.level}, {room.name}')
                if amount == 0: return # PARCHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                outputs.append((env.now, f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities[0].name} of the {room.name}...'))
                hotel.revenues[room] -= room.worker[1]
                hotel.budget -= room.worker[1]
                outputs.append((env.now, f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}'))
                #print(f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}')---------------------------------------
                
                bed.put(amount)
                outputs.append((env.now,(room.name, bed.level)))
                
                
                yield env.timeout(prm.HOUSEMAID_TIME)
                outputs.append((env.now, (room.name, bed.level, 'bbbbbbbbbbbbbbbbbbb')))
                room.using = False
                beliefs['working'] = False
                outputs.append((env.now, f'{env.now:6.1f} s: Housemaid finished and the room is clean'))
                outputs.append((env.now, f'Level after clean {room.name}: {bed.level}'))
    
    def action(hotel):
        hsd.brf(hotel, beliefs)
        hsd.generate_option(beliefs, desires)
        intentions = hsd.filter(desires)
        return intentions 
    time = env.now
    while time <  prm.SIM_TIME:
        while beliefs['working']:
            yield env.timeout(1)
        intention = action(hotel)
        
        env.process(execute_action(env, intention, hotel))
        time = env.now
        yield env.timeout(5)

    
def generic_worker(env, name, service, hotel):
    beliefs = gw.beliefs(service)
    desires = gw.desires(beliefs)

    def execute_action(env, service):
        if service == []:
            return
        beliefs['working'] = True
        
        with service[0].resource.request() as rq:
                service[0].using = True
                yield rq
                #print(f'{env.now:6.1f} s: Housemaid is cleaning the {service.utilities.name} of the {service.name}...')-----------------------------
                utility = service[0].utilities[0].container
                #print(utility.capacity, utility.level)
                amount = utility.capacity - utility.level
                print(f'total: {utility.capacity}, level: {utility.level}, {service[0].name}')
                if amount == 0: return # PARCHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                outputs.append((env.now, f'{env.now:6.1f} s: {name} is cleaning the {service[0].utilities[0].name} of the {service[0].name}...'))
                hotel.revenues[service[0]] = hotel.revenues[service[0]] - service[0].worker[1]
                hotel.budget -= service[0].worker[1]
                outputs.append((env.now, f'{env.now:6.1f} s: Level before clean the {service[0].name}: {utility.level}'))
                #print(f'{env.now:6.1f} s: Level before clean the {service.name}: {utility.level}')---------------------------------------
                
                utility.put(amount)
                outputs.append((env.now,(service[0].name, utility.level)))
                
                
                yield env.timeout(prm.HOUSEMAID_TIME)
                outputs.append((env.now, (service[0].name, utility.level, 'bbbbbbbbbbbbbbbbbbb')))
                service[0].using = False
                beliefs['working'] = False
                outputs.append((env.now, f'{env.now:6.1f} s: {name} finished and the service is clean'))
                outputs.append((env.now, f'Level after clean {service[0].name}: {utility.level}'))
    
    def action(hotel):
        gw.brf(hotel, beliefs)
        gw.generate_options(beliefs, desires)
        intentions = gw.filter(desires)
        return intentions
    
    time = env.now
    while time <  prm.SIM_TIME:
        while beliefs['working']:
            yield env.timeout(1)
        intention = action(hotel)
        
        env.process(execute_action(env, intention))
        time = env.now
        yield env.timeout(5)

def repairman(env, service, hotel):
    with service.resource.request() as rq:
                service.using = True
                yield rq
                #print(f'{env.now:6.1f} s: Housemaid is cleaning the {service.utilities.name} of the {service.name}...')-----------------------------
                #print(utility.capacity, utility.level)
                amount = prm.MAXIMUM_MAINTENANCE - service.maintenance
                if amount == 0: return # PARCHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                outputs.append((env.now, f'{env.now:6.1f} s: repairman is reapiring the {service}...'))
                
                outputs.append((env.now, f'{env.now:6.1f} s: Level before repair the {service.name}: {service.maintenance}'))
                #print(f'{env.now:6.1f} s: Level before clean the {service.name}: {utility.level}')---------------------------------------
                
                service.maintenance += amount
                #outputs.append((env.now,(service[0].name, utility.level)))              
                yield env.timeout(prm.REPAIRMAN_TIME)
                #outputs.append((env.now, (service.name, utility.level, 'bbbbbbbbbbbbbbbbbbb')))
                hotel.services[service] = True
                service.using = False
                outputs.append((env.now, f'{env.now:6.1f} s: repairman finished and the service is ready'))
                outputs.append((env.now, f'Level after repair {service.name}: {service.maintenance}'))
                hotel.budget -= random.randint(*prm.REPAIR)
     


###############################################################################
#------------------------- M   A   N   A   G   E   R --------------------------
###############################################################################

def manager(env, rooms, hotel):
    """Periodically check the clean level of the room and call the housemaid
       if the level falls below a threshold."""
    beliefs = mg.beliefs(hotel)
    desires = mg.desires()

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
        worker = env.process(generic_worker(env, service.name+'_worker', service, hotel))
        service.worker = [worker, random.randint(*prm.SALARIES)]
        yield env.timeout(1)
    
    def execute_action(env, intentions):
        if beliefs['wait']: return

        if intentions[0][1] in hotel.services or intentions[0][1] in hotel.rooms.services:
            print(intentions[0][0], intentions[0][1].name)
        else:
            print(intentions[0][0])
        if not intentions: return
        #print(intentions)
        for intention in intentions:
            if intention[0] == 'call_IA_Find':
                beliefs['working'] = True
                # Call the function of search
                outputs.append((env.now, f'Manager call the Find AI function'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False
            
            elif intention[0] == 'call_function_Survey':
                beliefs['working'] = True
                # Call the function of survey
                beliefs['hotel'].survey = env.now
                outputs.append((env.now, f'Manager call the Survey function'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False
                        
            elif intention[0] == 'raise_price':
                print('??????????@@@@@@@')
                beliefs['working'] = True
                old_price = intention[1].price
                intention[1].price += intention[1].price/10
                outputs.append((env.now, f'Manager raised the price of {intention[1].name}: {old_price} --> {intention[1].price}'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'lower_price':
                beliefs['working'] = True
                old_price = intention[1].price
                intention[1].price -= intention[1].price/10
                outputs.append((env.now, f'Manager lower the price of {intention[1].name}: {old_price} --> {intention[1].price}'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'close_service':
                beliefs['working'] = True
                hotel.services[intention[1]] = False
                outputs.append((env.now, f'Manager disable the {intention[1].name} service for strategy.'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'raise_salary':
                beliefs['working'] = True
                Lower_raise_salary(hotel, True)
                outputs.append((env.now, f'Manager raise the salaries.'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'lower_salary':
                beliefs['working'] = True
                Lower_raise_salary(hotel, False)
                outputs.append((env.now, f'Manager low the salaries.'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            if intention[0] == 'close_service_and_maintenance':
                beliefs['working'] = True
                service_ = intention[1]
                hotel.services[service_] = False
                outputs.append((env.now, f'Manager close the {service_.name} service for maintenance.'))
                desires[intention[2]][0] = False
                env.process(repairman(env, service_, hotel))
                yield env.timeout(10)
                beliefs['working'] = False

    def action():
        if beliefs['wait']: return
        mg.brf()
        mg.generate_options(beliefs, desires, env)
        intentions = mg.filter(beliefs, desires)
        return intentions
    
    time = env.now
    while time <  prm.SIM_TIME:
        if env.now >= prm.SIM_TIME/5: beliefs['wait'] = False

        if time - hotel.peak_season_time > prm.SEASON_TIME:
            hotel.peak_season = not hotel.peak_season
            hotel.peak_season_time = time
        while beliefs['working']:
            yield env.timeout(1)    
        intentions = action()  
        if not intentions:
            if not beliefs['wait']:
                print('NULL INTENTIOONNNNSSSS############')
            #print(intentions)
        env.process(execute_action(env, intentions))
        time = env.now
        yield env.timeout(40)



def Lower_raise_salary(hotel, operator):
    for room in hotel.rooms.services:
        if operator:
            room.worker[1] += room.worker[1]/10
        else:
            room.worker[1] -= room.worker[1]/10
    for service in hotel.services:
        if operator:
            service.worker[1] += service.worker[1]/10
        else:
            service.worker[1] += service.worker[1]/10
    if operator:
        prm.HOUSEMAID_TIME -= int(prm.HOUSEMAID_TIME/10)
    else:
        prm.HOUSEMAID_TIME += int(prm.HOUSEMAID_TIME/10)

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

# Execute!
env.run(until=prm.SIM_TIME)
for timestamp, mensaje in sorted(outputs, key = lambda outputs_: outputs_[0]):
        print(f"{timestamp}: {mensaje}")
