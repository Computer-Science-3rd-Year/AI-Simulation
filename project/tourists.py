import random
import params as prm
import enums as enu
import copy

services = {prm.energy: {prm.coffee, prm.rest_room, prm.energy_drink},
            prm.food: {prm.buffet, prm.snack_bar, prm.room_service, prm.restaurant, prm.ranchon},
            prm.fun: {prm.pool, prm.pool_table, prm.table_tennis, prm.tennis, prm.gym, prm.show_time},
            prm.comfort: {prm.ironing_service, prm.laundry_service}, #, prm.hair_salon, prm.steam_room}
            }


# servicios que un turista en particular necesita para satisfacer sus necesidades
def beliefs(hotel):
    update_services(hotel)
    #print(services)
    return {
            'energy_level': init_necesity_level(prm.TOURIST_ENERGY_LEVEL, prm.energy),
            'food_level':  init_necesity_level(prm.TOURIST_FOOD_LEVEL, prm.food),
            'fun_level': init_necesity_level(prm.TOURIST_FUN_LEVEL, prm.fun),
            'comfort_level': init_necesity_level(prm.TOURIST_COMFORT_LEVEL, prm.comfort),
            'has_room': False,
            'my_room': None,
            'room_cleanliness': None,
            'using_service': False,
            'restrictions': random.sample(prm.ATTRIBUTES, random.randint(0, len(prm.ATTRIBUTES))),
            'culture_level': random.randint(5, 100),
            'satisfaction': 0,
            'budget': random.randint(*prm.TOURIST_BUDGET),
            'complaints': 0,
            #----BELIEFS PARA LA ENCUESTA-----
            # 'room_features': None,    # alguno de los niveles que están en survey.py
            # 'room_clean_mainten': None,#  ''
            # 'general_quality': None, #  ''
            'used_services': [], # servicios usados por el turista
            # 'amenities_variety': None,
            # 'staff_friendliness': None,
            # 'quality_price': None
            }

def desires():
    return {
            'want_energy': False,
            'want_food': False,
            'want_fun': False,
            'want_comfort': False,
            'want_room': False,
            # 'be_honest': True,
            # 'do_survey': True,
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
    low_necesity_level(beliefs)

    claculate_satisfaction(beliefs, hotel.get_average_level_service(beliefs['used_services']))

def generate_option(beliefs, desires):
    if not beliefs['has_room']:
        desires['want_room'] = True
    elif beliefs['energy_level'][0] < prm.THRESHOLD_ENERGY:
        desires['want_energy'] = True
    elif beliefs['food_level'][0] < prm.THRESHOLD_FOOD:
        desires['want_food'] = True
    elif beliefs['fun_level'][0] < prm.THRESHOLD_FUN:
        desires['want_fun'] = True
    elif beliefs['comfort_level'][0] < prm.THRESHOLD_COMFORT:
        desires['want_comfort'] = True
    else:
        desires['want_fun'] = True

def filter(beliefs, desires, perception):
        none_intentions = False
        if beliefs['using_service']: return None

        if desires['want_room']:
            choiced_serv = 'reserve_room'
            necesity = prm.energy

        elif desires['want_energy']:
            necesity = prm.energy
            choiced_serv = choice_service_to_use(beliefs, perception, 'energy_level', necesity)
            # if intentions[0][0] == prm.rest_room and  (beliefs['my_room'] == 1 or beliefs['my_room'] == None or beliefs['my_room'].using):
            #     none_intentions = True

        elif desires['want_food']:
            necesity = prm.food
            choiced_serv = choice_service_to_use(beliefs, perception, 'food_level', necesity)

        elif desires['want_comfort']:
            necesity = prm.comfort
            choiced_serv = choice_service_to_use(beliefs, perception, 'comfort_level', necesity)

        elif desires['want_fun']:
            necesity = prm.fun
            choiced_serv = choice_service_to_use(beliefs, perception, 'fun_level', necesity)

        if none_intentions:
            intentions = None
        else:
            intentions = [(choiced_serv, necesity)]

        return intentions

def execute_action_(intentions, hotel, experience, name, outputs, len_of_stay, env, beliefs, desires):
        if not intentions or not intentions[0]:
            return
        my_room = beliefs['my_room']
        
        for intention in intentions:

            if intention[0] == 'reserve_room':
                env.process(reserve_room(env, hotel, name, beliefs, desires, len_of_stay))
                yield env.timeout(2)
                break

            elif intention[0] == 'rest_room':
                necesity_level = intention[1] + '_level'
                cant_required = prm.NECESITY_SIZE - beliefs[necesity_level][0]
                if cant_required > 0:
                    env.process(use_service(env, hotel, name, beliefs, desires, intention, my_room, outputs, experience, 'room', cant_required, necesity_level, False))
                yield env.timeout(2)
                break
                
            else:
                try:           
                    for service in hotel.services:
                        if service.name == intention[0]:

                            necesity_level = intention[1] + '_level'
                            cant_required = prm.NECESITY_SIZE - beliefs[necesity_level][0]

                            if '_' in service.name:
                                service_name = service.name.replace('_', ' ')
                            else: service_name = service.name
                            if cant_required > 0:
                                env.process(use_service(env, hotel, name, beliefs, desires, intention, service, outputs, experience, service_name, cant_required, necesity_level, False))
                            elif service.necesity == prm.fun:
                                env.process(use_service(env, hotel, name, beliefs, desires, intention, service, outputs, experience, service_name, cant_required, necesity_level, True))

                            yield env.timeout(2)
                            break
                except:
                    execute_action_(intentions, hotel, experience, name, outputs, len_of_stay, env, beliefs, desires)

def find_available_service(perception, necesity):
    for service in perception[necesity]:
        return service  

def room_clean_mainten_(beliefs):
    clean_level = 0
    for utility in beliefs['my_room'].utilities:
       clean_level += utility.container.level
        
    clean_level = clean_level/ len(beliefs['my_room'].utilities)

def claculate_satisfaction(beliefs, service_quality):
    sum_needs = 0
    necesities_count = 0
    for necesity in enu.Necesity:
        necesities_count += 1
        sum_needs += beliefs[necesity.name + '_level'][0]
    
    # Ponderación de las necesidades
    needs_score = sum_needs / necesities_count

    # Ponderación de las quejas
    complaint_score = beliefs['complaints'] * 0.25 #complaint_weight 

    # Ponderación de la calidad del servicio
    service_score = service_quality * 0.25 #service_weight

    # Cálculo final
    result = max(0, (needs_score + service_score - complaint_score) / 2)

    beliefs['satisfaction'] = result
    # result = max(0, sum_needs/necesities_count - 2*beliefs['complaints'])
    
    # beliefs['satisfaction'] = result

def update_services(hotel):
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
            services[prm.comfort].add(service.name)
        else:
            services[prm.fun].add(service.name)

def message_for_mainten(service, service_name):
    maintenance = service.maintenance
    if maintenance >= 80:
        return f'The {service_name} was in optimal maintenance conditions. '
    elif maintenance >= 60:
        return f'The {service_name} needs a bit of maintenance. '
    elif maintenance >= 40:
        return f'The {service_name} definitely needs maintenance. '
    elif maintenance >= 20:
        return f'The {service_name} needs a lot of maintenance. '
    else:
        return f'The {service_name} was in terrible maintenance conditions. '

def communicate(env, reserved, reserved_time, beliefs):
    if not beliefs['using_service']:
           for i in range(len(reserved) - 1, -1, -1):
               tuple = reserved[i]
               if not tuple[1]['my_room'] or tuple[1]['my_room'] == 1: continue
               if reserved_time[tuple[1]['my_room']] <= env.now: break
               if tuple[1]['culture_level'] < beliefs['culture_level']: continue
               for neces in enu.Necesity:
                   set_ = set(beliefs[neces.name+'_level'][1])
                   set.update(set(tuple[1][neces.name+'_level'][1]))
                   beliefs[neces.name+'_level'][1] = list(set_)
               #print('tourist is talking')
               break  

def reserve_room(env, hotel, name, beliefs, desires, len_of_stay):
    hotel.reserved.append((name, beliefs, len_of_stay))
    #print('RESERVE')
    beliefs['using_service'] = True
    yield env.timeout(100)
    beliefs['has_room'] = True
    desires['want_room'] = False
    beliefs['using_service'] = False
    if beliefs['my_room'] == None:
        beliefs['my_room'] = 1
    yield hotel.env.timeout(len_of_stay)

def use_service(env, hotel, name, beliefs, desires, intention, service, outputs, experience, service_name, cant_required, necesity_level, max_level):
    beliefs['using_service'] = True
    if not service in beliefs['used_services']: 
        beliefs['used_services'].append(copy.copy(service))

    with service.resource.request() as request_service:
        yield request_service
        if service.utilities[0].container.level >= cant_required/10:

            if service not in hotel.use_services:
                hotel.use_services[service] = 0   
             
            hotel.use_services[service] += 1

            if intention[0] != 'rest_room':
                price = service.price
                hotel.revenues[service] += price
                hotel.budget += price
                beliefs['budget'] -= price ##### PRESUPUESTO DEL TURISTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            outputs.append((env.now, f'El turista {name} accedió al servicio {service_name}, {beliefs[necesity_level][0]}'))
            
            if not max_level:
                beliefs[necesity_level][0] += cant_required
            
            desires['want_' + intention[1]] = False
            experience.append(message_for_mainten(service, service_name))
            #experience.append(f'The {service_name} of the hotel was good') #{random.choice(['excellent', 'very good', 'good', 'bad', 'very bad' ])}. ')
            service.maintenance -= random.randint(1, 2)
           
            yield hotel.env.timeout(random.randint(*prm.SPEED_OF_USING_SERVICE))
            
            beliefs['using_service'] = False
            if not max_level:
                if intention[0] != 'rest_room':
                    service.utilities[0].container.get(int(cant_required/10))
                else:
                    service.utilities[0].container.get(int(cant_required)) 
        else:
            hotel.complaints += 1
            beliefs['complaints'] += 1
            beliefs['using_service'] = False
            outputs.append((env.now, f'Servicio {service_name} con CLEAN LEVEL = {service.utilities[0].container.level}\n y {name} necesita {prm.NECESITY_SIZE - beliefs[necesity_level][0]} de energy'))
            #experience.append(f'The {service_name} of this hotel was not very good. ')
            experience.append(message_for_mainten(service, service_name))


    beliefs['using_service'] = False

def low_necesity_level(beliefs):
    for necesity in enu.Necesity:
        necesity_ = necesity.name + '_level'
        actual_level = beliefs[necesity_][0]

        cant = random.randint(*prm.REDUCE_NECESITY_LEVEL)
        actual_level = max(0,  actual_level - cant)

def choice_service_to_use(beliefs, perception, blfs_necesity, necesity):
    try:
        service = random.choice(list(set(beliefs[blfs_necesity][1]).intersection(set(perception[necesity]))))
    except:
        service = find_available_service(perception, necesity)
    return service

def init_necesity_level(range, necesity):
    level = random.randint(*range)

    if not services[necesity]:
        result = [level, services[necesity]]
    else:
        servs_list = random.sample(list(services[necesity]), random.randint(1, len(services[necesity])))
        result = [level, servs_list]
    return result