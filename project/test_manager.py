from simulation import *
import scipy.stats as stats

def best_strategy(test, active = True):
    result = []
    for i in range(100):

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


estrategy_for_limit = best_strategy(True)

estrategy_for_iter = best_strategy(True, False)

#Prueba de Mann-Whitney U
u_statistic, p_value = stats.mannwhitneyu(estrategy_for_limit, estrategy_for_iter)

print("\nPrueba de Mann-Whitney U:")
print("Estadístico U:", u_statistic)  # Mide la diferencia en los rangos de los datos
print("Valor p:", p_value)  # Probabilidad de obtener los resultados observados si no hay diferencia real

# Interpretación de los resultados:
alpha = 0.05  # Nivel de significancia

if p_value < alpha:
    print("\nExiste una diferencia significativa en la ganancia entre las estrategias.")
    print("Se rechaza la hipótesis nula de que no hay diferencia.")
    print("Podemos concluir que la estrategia que produjo los datos con mayor media es mejor.")
else:
    print("\nNo se encontró una diferencia significativa en la ganancia entre las estrategias.")
    print("Se acepta la hipótesis nula de que no hay diferencia.")
    print("No podemos concluir que una estrategia sea mejor que la otra.")
