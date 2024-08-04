import enums as enu

""" SIMULATION """
T_INTER = [30, 40]            # intervalo entre la llegada de los turistas     
SIM_TIME = 500            # tiempo total de la simulación     

""" NECESITY """
energy = enu.Necesity.energy.name
food = enu.Necesity.food.name
fun = enu.Necesity.fun.name

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

LEN_OF_STAY = [100, 200]  #   
SPEED_OF_USING_SERVICE = [10, 20]      # tiempo que demora usar un servicio determinado

""" WORKER """
HOUSEMAID_TIME = 15                  # tiempo que tarda la mucama en limpiar la habitación (segundos)   


""" MONEY """
SALARIES = {}                                                           
SALARIES['housemaid'] = 5

SALARIES_AMOUNT = {}             # salario cobrado por cada trabajador              
SALARIES_AMOUNT['housemaid'] = 0

AMOUNT = {}                    # pago acumulado por Los turistas en cada servicio
AMOUNT['room'] = 0                                                                 
AMOUNT['pool'] = 0
AMOUNT['buffet'] = 0
AMOUNT['bar'] = 0