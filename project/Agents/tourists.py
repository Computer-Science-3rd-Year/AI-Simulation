
beliefs = {
    'energy_level': float,
    'hunger_level': float,
    'fun_level': float,
    'comfort_level': float,
    'has_room': bool,
    'room_cleanliness': float,
}

desires = {
    'want_energy': bool,
    'want_food': bool,
    'want_fun': bool,
    'want_comfort': bool,
    'want_room': bool,
    }

def generate_option(beliefs, intentions):
    pass

def filter(beliefs, desires, intentions):
    pass

# conditions_of_rules_tourist = 
# {
#     if beliefs['has_room']:
#         beliefs['room_cleanliness'] = TOURIST_ROOMS[name].container.level,
#     if beliefs['energy_level'] >= TOURIST_ENERGY_SIZE:
#         desires['want_energy'] = False,
#     if beliefs['hunger_level'] >= TOURIST_HUNGER_SIZE:
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