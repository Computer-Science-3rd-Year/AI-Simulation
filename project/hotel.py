import simpy
import params as prm
import random


# ROOM_CLEANING_SIZE = 200       # máximo nive de limpieza de una habitación 
# THRESHOLD_CLEAN = 80           # mínimo de limpieza/confort (% del total)
class Hotel:
    def __init__(self, services, env, budget = 100, competition = 'media'):
        self.env = env
        self.services = {} # {'service_1': availability, 'service_2': availability,..., 'service_n': availability} *service_i existió en el hotel al menos 1 vez
        self.use_services = {}
        self.init_services(services)
        self.rooms = None
        self.init_rooms()
        self.revenues = {}
        self.init_revenues()
        self.expenses = {} # {'service_1': {'utility_1': expense, 'utility_2: expense',...},  'service_2': {'utility_1': expense, 'utility_2: expense',...}, ...} => 1 dict for each service
        self.init_expenses()
        self.tourist_register = {} # {'tourist_name': state_when_go, ...}  state == beliefs_del tourist
        self.peak_season = True
        self.peak_season_time = 0
        self.budget = budget
        self.demand = 0
        self.competition = competition
        self.survey = 0
        self.complaints = 0
        self.new_services = 0
        self.reserved = []
        self.reserved_bool = []
        self.reserved_time = {}
        self.experiences = {} # {'tourist_name': experience}
        self.reviews = {} # {'tourist_name': review}
        self.classifications = {} # {'tourist_name': calssifications of review}
    
    def init_services(self, services):
        for service in services:
            self.services[service] = True
            self.use_services[service] = 0
    
    def init_rooms(self):
        self.rooms = Services_set(self.env, 50, 'room', 'energy', ['bed'])#, Utility('bed', simpy.Container(self.env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE)))
    
    def init_revenues(self):
        for serv in self.services:
            self.revenues[serv] = 0
        for room in self.rooms.services:
            self.revenues[room] = 0

    def init_expenses(self):
        for serv in self.services:
            self.expenses[serv] = {}

            for utl in serv.utilities:
                self.expenses[serv][utl] = 0

        for serv in self.rooms.services:
            self.expenses[serv] = {}

            for utl in serv.utilities:
                self.expenses[serv][utl] = 0
     
    def add_service(self, new_service):
        if new_service in self.services:
            if self.services[new_service]: return
            self.services[new_service] = True
            return

        self.services[new_service] = True       
        self.revenues[new_service] = 0
        self.expenses[new_service] = {}

        for utility in new_service.utilities:
            self.expenses[utility] = 0

    
    def disable_service(self, old_service):
        if not old_service in self.services:
            return
        self.services[old_service] = False 

    def expenses_of_service(self, service):
        if not service in self.services and not service in self.rooms.services:
            return
        expense = 0
        for utility in service.utilities:
            expense += self.expenses[service][utility]
        
        return expense
    
    def get_average_level(self):
        total_level = 0
        for service in self.services:
            total_level += service.maintenance  #  Suponiendo que "level" es el atributo de la clase service
        return total_level / len(self.services)
    
    def get_average_level_service(self, services):
        total_level = 0
        for service in self.services:
            if not service in services: continue
            total_level += service.maintenance  #  Suponiendo que "level" es el atributo de la clase service
        return total_level / len(self.services)

    

class Service:
    def __init__(self, resource, name, necesity: str, utilities, price, cost = 70):
        self.resource = resource
        self.name = name
        self.necesity = necesity
        self.price = price
        self.utilities = utilities
        self.state = 0 # porcentaje de calidad de todas sus utilidades
        self.using = False
        self.worker = None
        self.maintenance = 100
        self.cost = cost
        self.attributes = self.attributes_()

    def update_state(self):
        for utlty in self.utilities:
            self.state += utlty.quality
        self.state = self.state/len(self.utilities)
    
    def update_price_from_state(self):
        for utlty in self.utilities:
            if utlty.quality < 0.5:
                price -= utlty.quality
            elif utlty.quality > 0.5:
                price += utlty.quality  
    
    def attributes_(self):
        return random.sample(prm.ATTRIBUTES, random.randint(0, len(prm.ATTRIBUTES)))

class Utility:
    def __init__(self, name, container): # podríamos agregarle partes, por ej: cama tiene colchón, sábanas, almohadas... 
                              # => calidad de la cama = sum(qual(colchon), qual(sabanas), qual(almohadas),...)
        self.name = name
        self.quality = 0.5 # porcentaje de 0 a 1, 1 equiv a 100% lo q equivale a lujo, luego 0.5 es estandar
                           # establecer un cálculo en base a, quizás, la opinión de los turistas, o pagar más dinero por aumentar la calidad 
        self.container = container

    def increment_quality(self):
        pass

class Services_set:
    def __init__(self, env, count_resources, name, necesity, utilities_name): #, utility: Utility =None):
        self.env = env
        self.service_name = name
        self.services = self.init_services(env, count_resources, name, necesity, utilities_name)#, utility)
    
    def init_services(self, env, count_resources, name, necesity, utilities_name): #, utility: Utility =None):
        services_ = {} #{'service_1': availability, 'service_2': avalability, ...}
        for i in range(count_resources):
            utilities = []
            for utility_name in utilities_name:
                utilities.append(Utility(utility_name, simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE)))
            service = Service(simpy.Resource(env, capacity=1), f'{name}_{i}', necesity, utilities, prm.ROOM_PRICE)
            services_[service] = True        
        return services_
