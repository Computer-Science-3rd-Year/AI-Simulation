
import random


NECESITY_SIZE = 100
NUMBER = 10
TOURIST_ENERGY_SIZE = 100        # nivel máximo de descanso
TOURIST_ENERGY_LEVEL = [20, 100]  # nivel inicial de energía de los turistas (menor_energía => más_sueño)
TOURIST_food_SIZE = 100        # nivel máximo de llenura por comida
TOURIST_food_LEVEL = [20, 100]  # nivel inicial de hambre de los turistas (menor_nivel => más_hambre)
TOURIST_FUN_SIZE = 100           # nivel máximo de diversión
TOURIST_FUN_LEVEL = [20, 100]     # nivel inicial de diversión de los turistas
TOURIST_COMFORT_SIZE = 100       # nivel máximo de confort
TOURIST_COMFORT_LEVEL = [20, 100] # nivel inicial de confort de los turistas (menor_energía => más_sueño)

services = {'energy': {'room', 'coffee', 'energy_drink', 'reserve_room'},
            'food': {'buffet', 'snack_bar', 'room_service', 'restaurant', 'ranchon'},
            'fun': {'pool', 'pool_table', 'table_tennis', 'tennis', 'gym', 'show_time'}
            }




# servicios que un turista en particular necesita para ssatisfacer sus necesidades
def beliefs():
    return {
            'energy_level': (random.randint(*TOURIST_ENERGY_LEVEL), set(random.sample(list(services['energy']), random.randint(1, len(services['energy'])))).update(['room'])),
            'food_level': (random.randint(*TOURIST_food_LEVEL), random.sample(list(services['food']), random.randint(1, len(services['food'])))),
            'fun_level': (random.randint(*TOURIST_FUN_LEVEL), random.sample(list(services['fun']), random.randint(1, len(services['fun'])))),
            #'comfort_level': random.randint(*TOURIST_COMFORT_LEVEL),
            'has_room': False,
            'room_cleanliness': None,
            }
def desires():
    return {
    'want_energy': False,
    'want_food': False,
    'want_fun': False,
    #'want_comfort': False,
    'want_room': False,
    }

def generate_option(tourist):
    if not tourist.beliefs['has_room']:
        tourist.desires['want_room'] = True
        return
    if tourist.beliefs['energy_level'][0] < 20:
        tourist.desires['want_energy'] = True
        return
    if tourist.beliefs['food_level'][0] < 20:
        tourist.desires['want_food'] = True
        return
    if tourist.beliefs['fun_level'][0] < 40:
        tourist.desires['want_fun'] = True
        return
    else:
        tourist.desires['want_food'] = True

def filter(tourist):
    if tourist.desires['want_room']:
        tourist.intentions = ('reserve_room', 'energy')
    if tourist.desires['want_energy']:
        tourist.intentions = (random.choice(set(tourist.beliefs['energy_level'][1]).intersection(tourist.perception['energy'])), 'energy')
    if tourist.desires['want_food']:
        tourist.intentions = (random.choice(set(tourist.beliefs['food_level'][1]).intersection(tourist.perception['food'])), 'food')
    if tourist.desires['want_fun']:
        tourist.intentions = (random.choice(set(tourist.beliefs['fun_level'][1]).intersection(tourist.perception['fun'])), 'fun')

def execute_action(tourist, intention, hotel):
    if tourist.intentions[0] == 'reserve_room':
        for room in hotel.rooms.services:
            if room.resource.count == 0:
                with room.request() as request_room:
                    yield request_room
                    tourist.beliefs['has_room'] = True
                    desires['want_room'] = False                            
                    # TOURIST_ROOMS[name] = room
                    # AMOUNT['room'] += PRICES['room']
                    print(f'El turista {tourist.name} accedió a la habitación {room.name}.')
                    yield hotel.env.timeout(20)
                    break  # Salir del bucle una vez que se reserve una habitación
        return
                
    for service in hotel.services:
        if service.name == intention[0]:
            necesity_level = intention[1] + '_level'
            cant_required = NECESITY_SIZE - tourist.beliefs[necesity_level]
            with service.resource.request() as request_service:
                yield request_service
                if service.resource.container.level >= cant_required:
                    yield service.resource.container.get(cant_required)
                    yield hotel.env.timeout(NUMBER)
                    tourist.beliefs[necesity_level] += cant_required
                    desires['want_' + intention[1]] = False





# conditions_of_rules_tourist = 
# {
#     if beliefs['has_room']:
#         beliefs['room_cleanliness'] = TOURIST_ROOMS[name].container.level,
#     if beliefs['energy_level'] >= TOURIST_ENERGY_SIZE:
#         desires['want_energy'] = False,
#     if beliefs['food_level'] >= TOURIST_food_SIZE:
#         desires['want_food'] = False
#     if beliefs['fun_level'] >= TOURIST_FUN_SIZE:
#         desires['want_fun'] = False
#     if beliefs['comfort_level'] >= TOURIST_COMFORT_SIZE:
#         desires['want_comfort'] = False

# }























class Tourist: # Agente BDI --> todas las funciones/componentes 
    def __init__(self, name, beliefs, desires, intentions, hotel):
        self.name = name
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions
        self.use_service = None
        self.init_use_service(hotel)
    
    def init_use_service(self, hotel):
        for serv in hotel.services:
            if serv[0].name == 'reception' and serv[1]:
                self.use_service = serv[0]
                break
        
        


# class Tourist(object):
#     def __init__(self, env, nombre, hotel):
#         self.env = env
#         self.nombre = nombre
#         self.hotel = hotel
#         self.action = env.process(self.run())
    
#     def run(self):
#         # El turista llega al hotel 
#         print(f'{self.env.now}: {self.nombre} llega al hotel')
#         # El turista reserva una habitación
#         with self.hotel.habitaciones.request() as req:
#             yield req
#             print(f'{self.env.now}: {self.nombre} se registra en la habitación')
#             yield self.env.timeout(2)  # Tiempo que el turista pasa en la habitación 
#             print(f'{self.env.now}: {self.nombre} sale del hotel') 

#         #tiempos_salida.append(self.env.now)  # Guarda el tiempo de salida del turista