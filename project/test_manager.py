from simulation import *
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

def best_strategy(test, active = True):
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
        
    return result


estrategy_on = best_strategy(True)

estrategy_off = best_strategy(True, False)

plt.figure(figsize=(8, 6))  # Ajusta el tamaño del gráfico
plt.hist(estrategy_on, bins=10, alpha=0.5, label="Con estrategia de negocio")
plt.hist(estrategy_off, bins=10, alpha=0.5, label="Sin estrategia de negocio")
plt.xlabel("Ganancias")
plt.ylabel("Frecuencia")
plt.title("Distribución de Ganancias por Estrategia")
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

#Prueba de Mann-Whitney U
u_statistic, p_value = stats.mannwhitneyu(estrategy_on, estrategy_off)

print("\nPrueba de Mann-Whitney U:")
print("Estadístico U:", u_statistic)  # Mide la diferencia en los rangos de los datos
print("Valor p:", p_value)  # Probabilidad de obtener los resultados observados si no hay diferencia real

# Interpretación de los resultados:
alpha = 0.05  # Nivel de significancia

mean_estrategy_on = np.mean(estrategy_on)
mean_estrategy_off = np.mean(estrategy_off)
estrategy_on_major = False

if mean_estrategy_on > mean_estrategy_off: estrategy_on_major = True


if p_value < alpha:
    print("\nExiste una diferencia significativa en la ganancia entre las estrategias.")
    print("Se rechaza la hipótesis nula de que no hay diferencia.")
    print("Podemos concluir que la estrategia que produjo los datos con mayor media es mejor.")
    if estrategy_on_major:
        print(f"Por tanto las estrategias tomadas por el manager genera mayores ganancias, con una ganancia media de {mean_estrategy_on}.")
    else:
        print(f"Por tanto las estrategias tomadas por el manager generan menos ganancias que si no las tomara. La ganancia media que reporta no tomar estas estrategias es de {mean_estrategy_off}.")
else:
    print("\nNo se encontró una diferencia significativa en la ganancia entre las estrategias.")
    print("No hay evidencia suficiente para rechazar la hipótesis nula de que no hay diferencia.")
    print("No podemos concluir que una estrategia sea mejor que la otra.")
    print(f"Ganancia media generada por las estrategias del manager: {mean_estrategy_on}\nGanancia media obtenida sin las estrategias del manager: {mean_estrategy_off}. ")


# if p_value < alpha:
#     print("\nExiste una diferencia significativa en la ganancia entre las estrategias.")
#     print("Se rechaza la hipótesis nula de que no hay diferencia.")
#     print("Podemos concluir que la estrategia que produjo los datos con mayor media es mejor.")
# else:
#     print("\nNo se encontró una diferencia significativa en la ganancia entre las estrategias.")
#     print("Se acepta la hipótesis nula de que no hay diferencia.")
#     print("No podemos concluir que una estrategia sea mejor que la otra.")
