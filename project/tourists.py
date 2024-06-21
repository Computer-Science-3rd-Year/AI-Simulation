class Tourist(object):
    def __init__(self, env, nombre, hotel):
        self.env = env
        self.nombre = nombre
        self.hotel = hotel
        self.action = env.process(self.run())
    
    def run(self):
        # El turista llega al hotel 
        print(f'{self.env.now}: {self.nombre} llega al hotel')
        # El turista reserva una habitación
        with self.hotel.habitaciones.request() as req:
            yield req
            print(f'{self.env.now}: {self.nombre} se registra en la habitación')
            yield self.env.timeout(2)  # Tiempo que el turista pasa en la habitación 
            print(f'{self.env.now}: {self.nombre} sale del hotel') 

        #tiempos_salida.append(self.env.now)  # Guarda el tiempo de salida del turista