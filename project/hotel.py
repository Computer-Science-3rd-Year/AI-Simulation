import simpy
import matplotlib.pyplot as plt

class Hotel:
    def __init__(self, env, num_habitaciones=10):
        self.env = env
        self.habitaciones = simpy.Resource(env, capacity=num_habitaciones)

# Crea el ambiente de simulación
env = simpy.Environment()
hotel = Hotel(env)

class Turista(object):
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

        tiempos_salida.append(self.env.now)  # Guarda el tiempo de salida del turista

# Crea algunos turistas
turista1 = Turista(env, "Juan", hotel)
turista2 = Turista(env, "Maria", hotel)
tiempos_salida = [] # Lista para guardar los tiempos de salida

# Ejecuta la simulación durante 10 horas
env.run(until=10)

# Visualización con matplotlib
plt.hist(tiempos_salida, bins=5, edgecolor='black')
plt.xlabel('Tiempo de salida')
plt.ylabel('Número de turistas')
plt.title('Salida de los turistas del hotel')
plt.show()