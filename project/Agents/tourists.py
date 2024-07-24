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