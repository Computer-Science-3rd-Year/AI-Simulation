import matplotlib.pyplot as plt
from simulation import *
import numpy as np

def best_strategy(test, uses_services, money_services, active = True):
    result = []
    for _ in range(100):
        prm.HOUSEMAID_TIME = 15
        prm.REPAIRMAN_TIME = 40
        env = simpy.Environment()
        services = basic_services(env)
        melia_hotel = hotel.Hotel(services, env)
        services_ = create_services(env)
        env.process(manager(env, melia_hotel.rooms.services, melia_hotel, services_, test, active))
        env.process(tourist_generator(env, melia_hotel))
        env.process(receptionist(env, melia_hotel))

        env.run(until=prm.SIM_TIME)
        result.append(melia_hotel.budget)
        for service in melia_hotel.services:
            if service in uses_services:
                uses_services[service].append(melia_hotel.use_services[service])
            else:
                uses_services[service] = [melia_hotel.use_services[service]]

            if service in money_services:
                money_services[service].append(melia_hotel.revenues[service])
            else:
                money_services[service] = [melia_hotel.revenues[service]]
    return result



uses_services = {}
money_service = {}
estrategy_for_limit = best_strategy(True, uses_services, money_service)

uses_services = {}
money_service = {}
estrategy_for_iter = best_strategy(False, uses_services, money_service)

plt.figure(figsize=(8, 6))  # Ajusta el tamaño del gráfico
plt.hist(estrategy_for_limit, bins=10, alpha=0.5, label="criterio_umbral")
plt.hist(estrategy_for_iter, bins=10, alpha=0.5, label="criterio_cant_iter")
plt.xlabel("Ganancias")
plt.ylabel("Frecuencia")
plt.title("Distribución de Ganancias por Estrategia")
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

#Prueba de Mann-Whitney U
u_statistic, p_value = stats.mannwhitneyu(estrategy_for_limit, estrategy_for_iter)

print("\nPrueba de Mann-Whitney U:")
print("Estadístico U:", u_statistic)  # Mide la diferencia en los rangos de los datos
print("Valor p:", p_value)  # Probabilidad de obtener los resultados observados si no hay diferencia real

# Interpretación de los resultados:
alpha = 0.05  # Nivel de significancia
media_estrategia_limit = np.mean(estrategy_for_limit)
media_estrategia_iter = np.mean(estrategy_for_iter)
limit_major = False

if media_estrategia_limit > media_estrategia_iter: limit_major = True


if p_value < alpha:
    print("\nExiste una diferencia significativa en la ganancia entre las estrategias.")
    print("Se rechaza la hipótesis nula de que no hay diferencia.")
    print("Podemos concluir que la estrategia que produjo los datos con mayor media es mejor.")
    if limit_major:
        print(f"Por tanto la estrategia que genera mayores ganancias es la que posee el criterio de parada por umbral con unan ganancia media de {media_estrategia_limit}.")
    else:
        print(f"Por tanto la estrategia que genera mayores ganancias es la que posee el criterio de parada por cantidad de iteraciones con unan ganancia media de {media_estrategia_iter}.")
else:
    print("\nNo se encontró una diferencia significativa en la ganancia entre las estrategias.")
    print("No hay evidencia suficiente para rechazar la hipótesis nula de que no hay diferencia.")
    print("No podemos concluir que una estrategia sea mejor que la otra.")
    print(f"Ganancia media con criterio de parada por umbral: {media_estrategia_limit}\nGanancia media con criterio de parada por cantidad de iteraciones: {media_estrategia_iter}. ")

names = []
values = []
values_price = []
for service in uses_services:
    result = sum(uses_services[service])/len(uses_services[service])
    if result > 30:
        names.append(service.name)
        values.append(result)
        values_price.append(service.price)

names_1 = []
values_1 = []
values_price_1 = []
for service in money_service:
    result = sum(money_service[service])/len(money_service[service])
    if result > 1700:
        names_1.append(service.name)
        values_1.append(result)
        values_price_1.append(service.price)

plt.bar(names, values)
plt.title("Popularidad")
plt.show()

plt.bar(names, values_price)
plt.title("Price of the most popular services")
plt.show()


plt.bar(names_1, values_1)
plt.title("Mayor Ganancia")
plt.show()

plt.bar(names_1, values_price_1)
plt.title("Price of highest profit services")
plt.show()