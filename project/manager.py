import random
import params as prm
import generic_worker as gw
from utils import *

# Creencias del hotel
def beliefs(hotel):
   beliefs_ = {}
   beliefs_['hotel'] = hotel
   beliefs_['working'] = False
   beliefs_['wait'] = False  # Esperar a que avance un poco la simulación
   beliefs_['nothing'] = False,
   return beliefs_

# Deseos del hotel
def desires():
    return {
        'maximize_revenue': False, # el resto forma parte de maximizar las ganancias. Por ahora es mejor  dividir los beliefs en medidas a corto y a largo plazo, realizar encuesta y dar mantenimiento
        'make_survey': False,        #realizar encuesta
        'raise_price': False,        # aumentar precio
        'lower_price': False,
        'close_service': False,
        'raise_salary': False,
        'lower_salary': False,
        'close_service_and_maintenance': [False, None],
    }

# Actualizar creencias basado en la percepción
def brf():
    pass
# Generar deseos basados en las creencias
def generate_options(beliefs, desires, env, hotel):
    # Ajustar deseos basados en las creencias
    #print(beliefs.budget)
    if beliefs['wait']: return
    beliefs_ = beliefs['hotel']
    occup_rooms = occupate_rooms(beliefs_)

    for service in beliefs_.services:
        if service.maintenance < prm.THRESHOLD_MAINTENANCE:
            desires['close_service_and_maintenance'] = [True, service]
            return 
    #print(beliefs_.budget)
    if beliefs_.budget <= prm.MINIMUM_BUDGET:
        if beliefs_.peak_season and occup_rooms > 0.5:
            #print('Manager!!!!!!!!!!!!')
            desires['raise_price'] = True
            return

        if not beliefs_.peak_season and occup_rooms < 0.30:
            desires['close_service'] = True
            return

        if not beliefs_.peak_season:
            desires['lower_price'] = True
            return

        if occup_rooms < 10:
            desires['lower_salary'] = True
            return
    
    elif hotel.complaints >= 4:
        #print(f'COMPLAINTS: {hotel.complaints}')
        desires['raise_salary'] = True
        hotel.complaints = 0

    # elif env.now - beliefs_.survey > prm.SURVEY_TIME:
    #     #print(f'{env.now} --> SURVEYYY')
    #     desires['make_survey'] = True
        
    elif beliefs_.budget > prm.MINIMUM_BUDGET and env.now - hotel.new_services > 300:
        hotel.new_services = env.now
        desires['maximize_revenue'] = True

    else:
        desires['nothing'] = True

# Generar intenciones basadas en los deseos y creencias
def filter(beliefs, desire):
    #print('ENTRO A FILTER EL MANAGAER')
    if beliefs['wait'] or beliefs['nothing']: return None
    hotel_ = beliefs['hotel']
    intentions = []

    if desire['maximize_revenue']:
        intentions.append(('call_IA_Find', 1, 'maximize_revenue'))
        return intentions
    
    if desire['make_survey']:
        intentions.append(('call_function_Survey', 1, 'make_survey'))
        return intentions
    
    if desire['raise_price']:
        service = calculate_service(hotel_, True)
        intentions.append(('raise_price', service, 'raise_price'))
        return intentions
    
    if desire['lower_price']:
        service = calculate_service(hotel_, False)
        intentions.append(('lower_price', service, 'lower_price'))
        return intentions
    
    if desire['close_service']:
        service = calculate_service(hotel_, False)
        if check(service, hotel_):
            intentions.append(('close_service', service, 'close_service'))
        else:
            return None
        return intentions
    
    if desire['raise_salary']:
        intentions.append(('raise_salary', 1, 'raise_salary'))
        return intentions

    if desire['lower_salary']:
        intentions.append(('lower_salary', 1, 'lower_salary'))
        return intentions
    
    if desire['close_service_and_maintenance'][0]:
        intentions.append(('close_service_and_maintenance', desire['close_service_and_maintenance'][1], 'close_service_and_maintenance'))
        return intentions
    return None

def execute_action(env, intentions, hotel, services_, outputs, beliefs, desires, test, active):
        if beliefs['wait'] or beliefs['nothing']: return
        if not intentions: return

        for intention in intentions:
            if intention[0] == 'call_IA_Find' and active:
                beliefs['working'] = True
                # Call the function of search
                outputs.append((env.now, f'Manager call the Find AI function'))
                desires[intention[2]] = False
                serv = AI_function_services(hotel, services_, test)
                if serv == None:
                    return
                for ser_ in serv:
                    if len(ser_) == 1:
                        hotel.use_services[ser_[0]] = 0
                        hotel.services[ser_[0]] = True
                        hotel.revenues[ser_[0]] = 0
                        hotel.expenses[ser_[0]] = {}
                        for utlty in ser_[0].utilities:
                            hotel.expenses[ser_[0]][utlty] = 0
                        worker = env.process(generic_worker(env, ser_[0].name+'_worker', ser_[0], hotel, outputs))
                        ser_[0].worker = [worker, random.randint(*prm.SALARIES)]
                    else:
                        hotel.services[ser_[1]] = True
                        if not ser_[1] in hotel.expenses:
                            hotel.services[ser_[1]] = True
                            hotel.use_services[ser_[1]] = 0
                            hotel.expenses[ser_[1]] = {}
                            hotel.revenues[ser_[1]] = 0
                            for utl in ser_[1].utilities:
                                hotel.expenses[ser_[1]][utl] = 0     
                        hotel.expenses[ser_[1]][ser_[0]] = 0 
                        worker = env.process(generic_worker(env, ser_[1].name+'_worker', ser_[1], hotel, outputs))
                        ser_[1].utilities.append(ser_[0])
                        ser_[1].worker = [worker, random.randint(*prm.SALARIES)]
                hotel.budget -= 200
                yield env.timeout(10)
                beliefs['working'] = False
            
            elif intention[0] == 'call_function_Survey' and active:
                beliefs['working'] = True
                # Call the function of survey
                beliefs['hotel'].survey = env.now
                outputs.append((env.now, f'Manager call the Survey function'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False
                        
            elif intention[0] == 'raise_price' and active:
                beliefs['working'] = True
                old_price = intention[1].price
                intention[1].price += intention[1].price/10
                outputs.append((env.now, f'Manager raised the price of {intention[1].name}: {old_price} --> {intention[1].price}'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'lower_price' and active:
                beliefs['working'] = True
                old_price = intention[1].price
                intention[1].price -= intention[1].price/10
                outputs.append((env.now, f'Manager lower the price of {intention[1].name}: {old_price} --> {intention[1].price}'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'close_service' and active:
                beliefs['working'] = True
                hotel.services[intention[1]] = False
                outputs.append((env.now, f'Manager disable the {intention[1].name} service for strategy.'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'raise_salary' and active:
                beliefs['working'] = True
                Lower_raise_salary(hotel, True)
                outputs.append((env.now, f'Manager raise the salaries.'))
                desires[intention[2]] = False
                yield env.timeout(10)
                beliefs['working'] = False

            elif intention[0] == 'lower_salary' and active:
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
                env.process(repairman(env, service_, hotel, outputs))
                yield env.timeout(10)
                beliefs['working'] = False

def generic_worker(env, name, service, hotel, outputs):
    beliefs = gw.beliefs(service)
    desires = gw.desires(beliefs)
    
    time = env.now
    while time <  prm.SIM_TIME:
        while beliefs['working']:
            yield env.timeout(1)
        gw.brf(hotel, beliefs)
        gw.generate_options(beliefs, desires)
        intentions = gw.filter(desires)
        
        env.process(gw.execute_action(env, intentions, beliefs, name, hotel, outputs))
        time = env.now
        yield env.timeout(5)

def repairman(env, service, hotel, outputs):
    with service.resource.request() as rq:
                service.using = True
                yield rq
                amount = prm.MAXIMUM_MAINTENANCE - service.maintenance
                if amount == 0: return 
                outputs.append((env.now, f'{env.now:6.1f} s: repairman is reapiring the {service.name}...'))
                
                outputs.append((env.now, f'{env.now:6.1f} s: Level before repair the {service.name}: {service.maintenance}'))
                service.maintenance += amount
                              
                yield env.timeout(prm.REPAIRMAN_TIME)
               
                hotel.services[service] = True
                service.using = False
                outputs.append((env.now, f'{env.now:6.1f} s: repairman finished and the service is ready'))
                outputs.append((env.now, f'Level after repair {service.name}: {service.maintenance}'))
                hotel.budget -= random.randint(*prm.REPAIR)  

