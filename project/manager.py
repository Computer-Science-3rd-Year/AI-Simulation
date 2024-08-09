import random
import params as prm


# Creencias del hotel
def beliefs(hotel):
   beliefs_ = {}
   beliefs_['hotel'] = hotel
   beliefs_['working'] = False
   beliefs_['wait'] = True  # Esperar a que avance un poco la simulación
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
        'close_service_and_maintenance': (False, None)
    }

# Actualizar creencias basado en la percepción
def brf():
    pass
# Generar deseos basados en las creencias
def generate_options(beliefs, desires, env):
    # Ajustar deseos basados en las creencias
    #print(beliefs.budget)
    if beliefs['wait']: return
    beliefs_ = beliefs['hotel']
    occup_rooms = occupate_rooms(beliefs_)

    if beliefs_.budget <= prm.MINIMUM_BUDGET:
        print(occup_rooms)
        if beliefs_.peak_season and occup_rooms > 0.5:
            print('Manager!!!!!!!!!!!!')
            desires['raise_price'] = True
            return

        elif not beliefs_.peak_season and occup_rooms < 0.45:
            desires['close_service'] = True
            return

        elif not beliefs_.peak_season:
            desires['lower_price'] = True
            return

        else:
            desires['lower_salary'] = True
            return

    for service in beliefs_.services:
        if service.maintenance < prm.THRESHOLD_MAINTENANCE:
            desires['close_service_and_maintenance'] = (True, service)
            return 
    
    if env.now - beliefs_.survey > prm.SURVEY_TIME:
        print(f'{env.now} --> SURVEYYY')
        desires['make_survey'] = True
            
    elif beliefs_.budget > prm.MINIMUM_BUDGET:
        desires['maximize_revenue'] = True

    else:
        desires['raise_salary'] = True


# Generar intenciones basadas en los deseos y creencias
def filter(beliefs, desire):
    #print('ENTRO A FILTER EL MANAGAER')
    if beliefs['wait']: return
    hotel_ = beliefs['hotel']
    intentions = []

    if desire['maximize_revenue']:
        intentions.append(('call_IA_Find', 1, 'maximize_revenue'))
        return intentions
    
    if desire['make_survey']:
        intentions.append(('call_function_Survey', 1, 'make_survey'))
        return intentions
    
    if desire['raise_price']:
        print('RAISE PRICE')
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
    

def occupate_rooms(hotel):
    count = 0
    for room in hotel.rooms.services:
        if room.resource.count == 0:
            continue
        count += 1
    return count/len(hotel.rooms.services)

def calculate_service(hotel, operator):
    if operator:
        max_revenue = 0
    else:
        max_revenue = 1000000000000
    service_return = None
    for service in hotel.revenues:
        if not service in hotel.rooms.services and hotel.services[service]:
            value = hotel.revenues[service]
            cost = hotel.expenses_of_service(service)
            if value - cost >= max_revenue and operator:
                max_revenue = value - cost
                service_return = service
            if value - cost <= max_revenue and not operator:
                max_revenue = value - cost
                service_return = service
    return service_return

def check(service, hotel):
    necesity = service.necesity
    count = 0
    for serv in hotel.services:
        if serv.necesity == necesity and hotel.services[service]:
            count += 1
    
    return count > 1