import random
import params as prm


# Creencias del hotel
def beliefs(hotel):
   return hotel

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
    if beliefs.budget <= prm.MINIMUM_BUDGET:
        print(occupate_rooms(beliefs))
        if beliefs.peak_season and occupate_rooms(beliefs) > 0.5:
            print('Manager!!!!!!!!!!!!')
            desires['raise_price'] = True
            return

        elif not beliefs.peak_season and occupate_rooms(beliefs) < 0.45:
            desires['close_service'] = True
            return

        elif not beliefs.peak_season:
            desires['lower_price'] = True
            return

        else:
            desires['lower_salary'] = True
            return

    for service in beliefs.services:
        if service.maintenance < prm.THRESHOLD_MAINTENANCE:
            desires['close_service_and_maintenance'] = (True, service)
            return 
    
    if env.now - beliefs.survey > prm.SURVEY_TIME:
        print('SURVEYYY')
        desires['make_survey'] = True
            
    elif beliefs.budget > prm.MINIMUM_BUDGET:
        desires['maximize_revenue'] = True


    else:
        desires['raise_salary'] = True


# Generar intenciones basadas en los deseos y creencias
def filter(beliefs, desire):
    #print('ENTRO A FILTER EL MANAGAER')
    intentions = []
    if desire['maximize_revenue']:
        intentions.append(('call_IA_Find', 1, 'maximize_revenue'))
        return intentions
    
    if desire['make_survey']:
        intentions.append(('call_function_Survey', 1, 'make_survey'))
        return intentions
    
    if desire['raise_price']:
        print('RAISE PRICE')
        service = calculate_service(beliefs, True)
        intentions.append(('raise_price', service, 'raise_price'))
        return intentions
    
    if desire['lower_price']:
        service = calculate_service(beliefs, False)
        intentions.append(('lower_price', service, 'lower_price'))
        return intentions
    
    if desire['close_service']:
        service = calculate_service(beliefs, False)
        if check(service, beliefs):
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