beliefs = {}
desires = {}

def brf(beliefs, perception):
    pass

def generate_option(beliefs, intentions):
    pass

def filter(beliefs, desires, intentions):
    pass

# class Manager:
#     def __init__(self, hotel):
#         self.hotel = hotel
#         self.estrategia = {
#             "atracciones": [],
#             "servicios": [],
#             "personal": [],
#         }
#         self.metas = {
#             "ingresos": 0,
#             "satisfaccion_turistas": 0,
#             "reputacion": 0,
#         }

#     def evaluar_resultados(self):
#         """
#         Evalúa la situación actual del hotel.
#         """
#         ingresos = self.hotel.calcular_ingresos()
#         satisfaccion = self.hotel.calcular_satisfaccion_turistas()
#         reputacion = self.hotel.calcular_reputacion()
#         self.metas["ingresos"] = ingresos
#         self.metas["satisfaccion_turistas"] = satisfaccion
#         self.metas["reputacion"] = reputacion

#     def tomar_decisiones(self):
#         """
#         Toma decisiones basadas en reglas simples.
#         """
#         # Reglas básicas de negocio
#         if self.metas["ingresos"] < self.hotel.ingresos_objetivo:
#             if self.metas["reputacion"] < 5:
#                 self.hotel.agregar_atraccion("Bar")
#                 self.estrategia["atracciones"].append("Bar")
#             else:
#                 self.hotel.contratar_trabajador("Bartender")
#                 self.estrategia["personal"].append("Bartender")
#         if self.metas["satisfaccion_turistas"] < 7:
#             self.hotel.mejorar_servicios()
#             self.estrategia["servicios"].append("Mejorar calidad")

#     def ejecutar_estrategia(self):
#         """
#         Ejecuta la estrategia del Manager
#         """
#         self.evaluar_resultados()
#         self.tomar_decisiones()

