import params as prm

def beliefs(service):
    dict_ = {}
    dict_['service'] = [service, service.utilities[0].container.level, True]# the first bool is for the disponiblity in hotel
    dict_['working'] = False
    return dict_

def desires(beliefs):
    dict_ = {}
    service = beliefs['service'][0] 
    dict_[service] = False
    return dict_

def brf(hotel, beliefs):
    service = beliefs['service'][0]
    beliefs['service'][1] = service.utilities[0].container.level
    beliefs['service'][2] = hotel.services[service]

def generate_options(beliefs, desires):
    service = beliefs['service'][0]
    if  service.utilities[0].container.level < prm.THRESHOLD_CLEAN:
        desires[service] = True

def filter(desires):
    intentions = []
    for service in desires:
        if desires[service]:
            intentions.append(service)
    return intentions

def execute_action(env, service, beliefs, name, hotel, outputs):
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
            #print(f'total: {utility.capacity}, level: {utility.level}, {service[0].name}')
            if amount == 0: return # PARCHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            outputs.append((env.now, f'{env.now:6.1f} s: {name} is working on the {service[0].utilities[0].name} of the {service[0].name}...'))
            hotel.revenues[service[0]] = hotel.revenues[service[0]] - service[0].worker[1]
            hotel.budget -= service[0].worker[1]
            outputs.append((env.now, f'{env.now:6.1f} s: Level before work the {service[0].name}: {utility.level}'))
            #print(f'{env.now:6.1f} s: Level before clean the {service.name}: {utility.level}')---------------------------------------
            
            utility.put(amount)
            #outputs.append((env.now,(service[0].name, utility.level)))
            
            
            yield env.timeout(4)
            #outputs.append((env.now, (service[0].name, utility.level, 'bbbbbbbbbbbbbbbbbbb')))
            service[0].using = False
            beliefs['working'] = False
            outputs.append((env.now, f'{env.now:6.1f} s: {name} finished and the {service[0].name} is ready'))
            outputs.append((env.now, f'Level after clean {service[0].name}: {utility.level}'))