import enums as enu

""" SIMULATION """
T_INTER = [5, 20]            # intervalo entre la llegada de los turistas     
SIM_TIME = 1000            # tiempo total de la simulación     

""" NECESITY """
energy = enu.Necesity.energy.name
food = enu.Necesity.food.name
fun = enu.Necesity.fun.name
comfort = enu.Necesity.comfort.name

""" SERVICE """
rest_room = enu.Services_name.rest_room.name
coffee = enu.Services_name.coffee.name
energy_drink = enu.Services_name.energy_drink.name
buffet = enu.Services_name.buffet.name
snack_bar = enu.Services_name.snack_bar.name
room_service = enu.Services_name.room_service.name
restaurant = enu.Services_name.restaurant.name
ranchon = enu.Services_name.ranchon.name
pool = enu.Services_name.pool.name
pool_table = enu.Services_name.pool_table.name
table_tennis = enu.Services_name.table_tennis.name
tennis = enu.Services_name.tennis.name
gym = enu.Services_name.gym.name
show_time = enu.Services_name.show_time.name

""" SERVICES """
MAXIMUM_MAINTENANCE = 100
THRESHOLD_MAINTENANCE = 70


""" ROOM """
ROOM_CLEANING_SIZE = 100       # máximo nive de limpieza de una habitación         
THRESHOLD_CLEAN = 95           # mínimo de limpieza/confort (% del total)        

""" POOL """
POOL_CLEANING_SIZE = 100       # máximo nive de limpieza de una habitación       
THRESHOLD_CLEAN = 50           # mínimo de limpieza/confort (% del total)        

""" TOURIST """
NECESITY_SIZE = 100                                      
TOURIST_ENERGY_LEVEL = [20, 50]  # nivel inicial de energía de los turistas (menor_energía => más_sueño)  
TOURIST_FOOD_LEVEL = [20, 50]   # nivel inicial de hambre de los turistas (menor_nivel => más_hambre)    
TOURIST_FUN_LEVEL = [20, 50]      # nivel inicial de diversión de los turistas                             
TOURIST_COMFORT_LEVEL = [20, 50] # nivel inicial de confort de los turistas (menor_energía => más_sueño)
THRESHOLD_ENERGY = 50
THRESHOLD_FOOD = 60
THRESHOLD_FUN = 40
ATTRIBUTES = ['pool', 'TV', 'safe', 'jacuzzi', 'bar', 'stunning_view', 'balcony']

LEN_OF_STAY = [100, 300]  #   
SPEED_OF_USING_SERVICE = [10, 20]      # tiempo que demora usar un servicio determinado

""" WORKER """
HOUSEMAID_TIME = 15                  # tiempo que tarda la mucama en limpiar la habitación (segundos)
REPAIRMAN_TIME = 40 


""" MONEY """
SALARIES = [70, 90]
REVENUE_TARGET = 10
REPUTATION_TARGET = 80
MINIMUM_BUDGET = 300  # en % lo más probable
STABLE_BUDGET = 80 
REPAIR = [10, 17]
ROOM_PRICE = 50
COFFEE_PRICE = 5
ENERGY_DRINK_PRICE = 10
BUFFET_PRICE = 100
SNACK_BAR_PRICE = 25
ROOM_SERVICE_PRICE = 70
RESTAURANT_PRICE = 150
RANCHON_PRICE = 65
POOL_PRICE = 30
POOL_TABLE_PRICE = 10
TABLE_TENNIS_PRICE = 10
TENNIS_PRICE = 25
GYM_PRICE = 20
SHOW_TIME_PRICE = 50
IRONING_SERVICE_PRICE = 45
GENERIC_PRICE = 40
TOURIST_BUDGET = [1000000, 1500000]

""" SURVEY """
SURVEY_TIME = 400

"""HOTEL"""
SEASON_TIME = 300

SALARIES_AMOUNT = {}             # salario cobrado por cada trabajador              
SALARIES_AMOUNT['housemaid'] = 0

AMOUNT = {}                    # pago acumulado por Los turistas en cada servicio
AMOUNT['room'] = 0                                                                 
AMOUNT['pool'] = 0
AMOUNT['buffet'] = 0
AMOUNT['bar'] = 0