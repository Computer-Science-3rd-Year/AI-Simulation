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


