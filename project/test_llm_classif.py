import enums as enu
from simulation import *
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import numpy as np
import pandas as pd

def llm_and_real_classification():
    result = [] #[(real_classif, llm_classif), ...]
    for _ in range(10):
        melia_hotel = run_simulation()

        for tourist in melia_hotel.tourist_register:
            llm_classif = replace_(melia_hotel.classifications[tourist])
            real_classif = melia_hotel.tourist_register[tourist]['satisfaction']
            services_level = melia_hotel.get_average_level()  # Obtener nivel de servicio
            result.append((real_classif, llm_classif, services_level)) # (int, string, float)

    return result

def compare_classifications(real, llm, reals, llm_classif):
    #llm_classif_name = replace_(llm)
    llm_classif.append(enu.Satisfaction_classif[llm].value)

    if real <= 20:
        real_classif_name = enu.Satisfaction_classif['very_bad'].name
        reals.append(0)

    elif real > 20 and real <= 40:
        real_classif_name = enu.Satisfaction_classif['bad'].name
        reals.append(1)

    elif real > 40 and real <= 60:
        real_classif_name = enu.Satisfaction_classif['good'].name
        reals.append(2)

    elif real > 60 and real <= 80:
        real_classif_name = enu.Satisfaction_classif['very_good'].name
        reals.append(3)

    else:
        real_classif_name = enu.Satisfaction_classif['excellent'].name
        reals.append(4)

    if llm == real_classif_name: return 1, real_classif_name
    return 0, real_classif_name

def replace_(str):
    if '_' in str: return str.replace('_', ' ')
    elif ' ' in str: return str.replace(' ', '_')
    return str

result = llm_and_real_classification()
reals = []
llm_classif = []
total = 0
asserts = 0
errors = []
error_differences = []

for real, llm_, services_level in result:
    correct = compare_classifications(real, llm_, reals, llm_classif)
    total += 1
    if correct[0]:
        asserts += 1
    else:
        errors.append((correct[1], llm_))
        error_differences.append(abs(reals[-1] - llm_classif[-1]))

# 1. Histograma de Clasificación Real vs. LLM
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)  # 2 filas, 2 columnas, posición 1
plt.hist(reals, bins=5, edgecolor='black', label='Clasificación Real')
plt.hist(llm_classif, bins=5, edgecolor='black', label='Clasificación LLM', alpha=0.7)
plt.title("Histograma de Clasificación Real vs. LLM")
plt.xlabel("Categorías de Satisfacción")
plt.ylabel("Frecuencia")
plt.xticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
plt.legend()

# 2. Gráfica de Pastel de Aserción
plt.subplot(2, 2, 2)  # 2 filas, 2 columnas, posición 2
labels = ["Aserción", "Error"]
sizes = [asserts, len(errors)]
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
plt.title("Porcentaje de Aserción vs. Error")

data = {
    'satisfaction_real': reals,
    'llm_classification': llm_classif
}
df = pd.DataFrame(data)

# Realizando el ANOVA
f_statistic, p_value = stats.f_oneway(df['satisfaction_real'], df['llm_classification'])


alpha = 0.05
# Interpretación de los resultados
if p_value < alpha:
    interpretacion = (
        f"El valor p ({p_value:.3f}) es menor que el nivel de significancia ({alpha}). "
        f"Se rechaza la hipótesis nula. Existe evidencia estadística de que las clasificaciones del LLM "
        f"y la satisfacción real de los turistas son diferentes."
    )
else:
    interpretacion = (
        f"El valor p ({p_value:.3f}) es mayor que el nivel de significancia ({alpha}). "
        f"No se rechaza la hipótesis nula. No hay evidencia estadística suficiente para afirmar que "
        f"las clasificaciones del LLM y la satisfacción real de los turistas son diferentes."
    )
    
# Imprimir los resultados
print(f"Valor F: {f_statistic:.2f}")
print(f"Valor p: {p_value:.3f}")
print(interpretacion)

# Generar diagrama de cajas
plt.boxplot([df['satisfaction_real'], df['llm_classification']], labels=['Real', 'LLM'])
plt.title('Comparación de Clasificaciones')
plt.ylabel('Clasificación')
plt.show()

# Generar un histograma
plt.hist(df['satisfaction_real'], bins=5, alpha=0.5, label='Real')
plt.hist(df['llm_classification'], bins=5, alpha=0.5, label='LLM')
plt.title('Frecuencia de Clasificaciones')
plt.xlabel('Clasificación')
plt.ylabel('Frecuencia')
plt.legend()
plt.show()

# Generar un diagrama de dispersión
plt.scatter(df['satisfaction_real'], df['llm_classification'])
plt.title('Relación entre Clasificaciones')
plt.xlabel('Satisfacción Real')
plt.ylabel('Clasificación del LLM')
plt.show()


# # 3. Matriz de Correlación
# plt.subplot(2, 2, 3)  # 2 filas, 2 columnas, posición 3
# correlation, p_value = spearmanr(reals, llm_classif)
# corr_matrix = np.array([[1, correlation], [correlation, 1]])
# plt.imshow(corr_matrix, cmap='Blues')
# plt.colorbar()
# plt.xticks(range(2), ['Clasificación Real', 'Clasificación LLM'])
# plt.yticks(range(2), ['Clasificación Real', 'Clasificación LLM'])
# plt.title("Matriz de Correlación de Spearman")

# # 4. Gráfica de Dispersión con Líneas de Referencia
# plt.subplot(2, 2, 4)  # 2 filas, 2 columnas, posición 4
# plt.scatter(reals, llm_classif, s=50, c='blue', alpha=0.7)
# plt.title("Aserción de la Clasificación del LLM")
# plt.xlabel("Clasificación Real")
# plt.ylabel("Clasificación del LLM")
# plt.xticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
# plt.yticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
# plt.grid(True)
# # Líneas de referencia para indicar una clasificación perfecta
# plt.plot([0, 4], [0, 4], color='red', linestyle='--')

# plt.tight_layout()
# plt.show()

# # Gráfica de Aserción
# plt.figure(figsize=(8, 6))
# plt.scatter(reals, llm_classif, s=50, c='blue', alpha=0.7)
# plt.title("Aserción de la Clasificación del LLM")
# plt.xlabel("Clasificación Real")
# plt.ylabel("Clasificación del LLM")
# plt.xticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
# plt.yticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
# plt.grid(True)
# plt.show()

# Análisis de Errores
print(f"Total de Clasificaciones: {total}")
print(f"Aserciones: {asserts}")
print(f"Errores: {len(errors)}")
print(f"Porcentaje de Aserción: {asserts/total:.2%}")

# Diferencias en los Errores
print("nDiferencias en los Errores:")
for i, error in enumerate(errors):
    print(f"Error {i+1}: Real: {enu.Satisfaction_classif[error[0]].name}, LLM: {enu.Satisfaction_classif[error[1]].name} - Diferencia: {error_differences[i]}")

# Correlación con Servicios del Hotel
correlation, p_value = spearmanr(reals, llm_classif)
print(f"nCorrelación de Spearman entre Clasificación Real y del LLM: {correlation:.3f} (P-value: {p_value:.3f})")
correlation_services, p_value_services = spearmanr(reals, [services_level for _, _, services_level in result])
print(f"Correlación de Spearman entre Clasificación Real y Nivel de Servicios: {correlation_services:.3f} (P-value: {p_value_services:.3f})")

# Correlación con Servicios del Hotel
correlation_services, p_value_services = spearmanr(reals, [services_level for _, _, services_level in result])
print(f"Correlación de Spearman entre Clasificación Real y Nivel de Servicios: {correlation_services:.3f} (P-value: {p_value_services:.3f})")

# Gráfica de Correlación
plt.figure(figsize=(8, 6))
plt.scatter(reals, [services_level for _, _, services_level in result], s=50, c='blue', alpha=0.7)
plt.title("Correlación entre Clasificación Real y Nivel de Servicios")
plt.xlabel("Clasificación Real")
plt.ylabel("Nivel de Servicios")
plt.xticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
plt.grid(True)
plt.show()

# --- Gráficas para el Análisis de Diferencias de Errores ---

# 1. Histograma de Diferencias de Errores
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.hist(error_differences, bins=5, edgecolor='black')
plt.title("Histograma de Diferencias de Errores")
plt.xlabel("Diferencia Absoluta entre Clasificaciones")
plt.ylabel("Frecuencia")

# 2. Gráfica de Pastel de Diferencias de Errores
plt.subplot(2, 2, 2)
unique_differences, counts = np.unique(error_differences, return_counts=True)
plt.pie(counts, labels=unique_differences, autopct="%1.1f%%", startangle=90)
plt.title("Distribución de Diferencias de Errores")

# 4. Gráfica de Dispersión de Errores
plt.subplot(2, 2, 4)
plt.scatter([i for i in range(len(errors))], error_differences, s=50, c='blue', alpha=0.7)
plt.title("Diferencias de Errores en Cada Clasificación")
plt.xlabel("Número de Error")
plt.ylabel("Diferencia Absoluta entre Clasificaciones")

plt.tight_layout()
plt.show()

# --- Gráficas para el Análisis de Servicios ---

# 1. Histograma de Clasificación Real vs. Servicios
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.hist(reals, bins=5, edgecolor='black', label='Clasificación Real')
plt.hist([services_level for _, _, services_level in result], bins=5, edgecolor='black', label='Nivel de Servicios', alpha=0.7)
plt.title("Histograma de Clasificación Real vs. Nivel de Servicios")
plt.xlabel("Categorías de Satisfacción / Nivel de Servicios")
plt.ylabel("Frecuencia")
plt.xticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
plt.legend()

# 3. Matriz de Correlación
plt.subplot(2, 2, 3)
correlation_services, p_value_services = spearmanr(reals, [services_level for _, _, services_level in result])
corr_matrix = np.array([[1, correlation_services], [correlation_services, 1]])
plt.imshow(corr_matrix, cmap='Blues')
plt.colorbar()
plt.xticks(range(2), ['Clasificación Real', 'Nivel de Servicios'])
plt.yticks(range(2), ['Clasificación Real', 'Nivel de Servicios'])
plt.title("Matriz de Correlación de Spearman")

# 4. Gráfica de Dispersión
plt.subplot(2, 2, 4)
plt.scatter(reals, [services_level for _, _, services_level in result], s=50, c='blue', alpha=0.7)
plt.title("Relación entre Clasificación Real y Nivel de Servicios")
plt.xlabel("Clasificación Real")
plt.ylabel("Nivel de Servicios")
plt.xticks(range(5), ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
plt.grid(True)

plt.tight_layout()
plt.show()