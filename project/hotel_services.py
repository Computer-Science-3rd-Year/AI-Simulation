import hotel
import params as prm
import simpy
import random

env = simpy.Environment()
rest_room = hotel.Service(simpy.Resource(env, capacity = 10), 'rest_room', prm.energy, [hotel.Utility('bed', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.ROOM_PRICE)
pool = hotel.Service(simpy.Resource(env, capacity=11), 'pool', prm.fun, [hotel.Utility('pool_utl', simpy.Container(env, prm.POOL_CLEANING_SIZE, init=prm.POOL_CLEANING_SIZE))], prm.POOL_PRICE)
coffee = hotel.Service(simpy.Resource(env, capacity=4), 'coffee', prm.energy, [hotel.Utility('bar_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.COFFEE_PRICE)
energy_drink = hotel.Service(simpy.Resource(env, capacity=4), 'energy_drink', prm.energy, [hotel.Utility('bar_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.ENERGY_DRINK_PRICE)
buffet = hotel.Service(simpy.Resource(env, capacity = 10), 'buffet', prm.food, [hotel.Utility('buffet', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], prm.BUFFET_PRICE)
snack_bar = hotel.Service(simpy.Resource(env, capacity = 7), 'snack_bar', prm.food, [hotel.Utility('snack_bar', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.SNACK_BAR_PRICE)
room_service = hotel.Service(simpy.Resource(env, capacity = 11), 'room_service', prm.food, [hotel.Utility('room_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.ROOM_SERVICE_PRICE)
restaurant = hotel.Service(simpy.Resource(env, capacity = 7), 'restaurant', prm.food, [hotel.Utility('restaurant', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.RESTAURANT_PRICE)
ranchon = hotel.Service(simpy.Resource(env, capacity = 5), 'ranchon', prm.food, [hotel.Utility('ranchon', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.RANCHON_PRICE)
pool_table = hotel.Service(simpy.Resource(env, capacity = 2), 'pool_table', prm.fun, [hotel.Utility('pool_table', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.POOL_TABLE_PRICE)
table_tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'table_tennis', prm.fun, [hotel.Utility('table_tennis', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.TABLE_TENNIS_PRICE)
tennis = hotel.Service(simpy.Resource(env, capacity = 2), 'tennis', prm.fun, [hotel.Utility('tennis', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.TENNIS_PRICE)
gym = hotel.Service(simpy.Resource(env, capacity = 11), 'gym', prm.fun, [hotel.Utility('gym', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.GYM_PRICE)
show_time = hotel.Service(simpy.Resource(env, capacity = 11), 'show_time', prm.fun, [hotel.Utility('show_time', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init=prm.ROOM_CLEANING_SIZE))], prm.SHOW_TIME_PRICE)

#pool = hotel.Service(simpy.Resource(env, capacity=11), 'pool', prm.fun, [hotel.Utility('pool_utl', simpy.Container(env, prm.POOL_CLEANING_SIZE, init=prm.POOL_CLEANING_SIZE))], prm.POOL_PRICE)
ironing_service = hotel.Service(simpy.Resource(env, capacity= 7), 'ironing_service', prm.comfort,[hotel.Utility('ironing_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], prm.IRONING_SERVICE_PRICE, 40)
laundry_service = hotel.Service(simpy.Resource(env, capacity= 10), 'laundry_service', prm.comfort,[hotel.Utility('laundry_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 50)
wi_fi = hotel.Service(simpy.Resource(env, capacity= 10), 'wi_fi', prm.fun,[hotel.Utility('wi_fi_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 71)
transfer_service = hotel.Service(simpy.Resource(env, capacity= 10), 'transfer_service', prm.comfort,[hotel.Utility('transfer_utl', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 20)   
excursion = hotel.Service(simpy.Resource(env, capacity= 10), 'excursion', prm.fun,[hotel.Utility('excursion', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 100)
souvenir_shopping = hotel.Service(simpy.Resource(env, capacity= 10), 'souvenir_shopping', prm.comfort,[hotel.Utility('souvenir_shopping', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 20)
continental_breakfast = hotel.Utility('continental_breakfast', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))
buffet_breakfast = hotel.Utility('buffet_breakfast', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))
carte_breakfast = hotel.Utility('carte_breakfast', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))
carte_dinner = hotel.Utility('carte_dinner', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))
#########################################################################
tasting_menu = hotel.Utility('tasting_menu', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))
local_cuisine_restaurant = hotel.Service(simpy.Resource(env, capacity= 10), 'local_cuisine_restaurant', prm.food,[hotel.Utility('local_cuisine_restaurant', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 80)
International_cuisine_restaurant = hotel.Service(simpy.Resource(env, capacity= 10), 'International_cuisine_restaurant', prm.food,[hotel.Utility('International_cuisine_restaurant', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 90)
bar = hotel.Service(simpy.Resource(env, capacity= 10), 'bar', prm.food,[hotel.Utility('bar', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 30)
pool_bar = hotel.Service(simpy.Resource(env, capacity= 10), 'pool_bar', prm.food,[hotel.Utility('pool_bar', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 35)
information_bureau = hotel.Service(simpy.Resource(env, capacity= 10), 'information_bureau', prm.comfort,[hotel.Utility('information_bureau', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 15)
spa = hotel.Service(simpy.Resource(env, capacity= 10), 'spa', prm.fun,[hotel.Utility('spa', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 75)
masaje = hotel.Service(simpy.Resource(env, capacity= 10), 'masaje', prm.fun,[hotel.Utility('masaje', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 70)
facial_treatments = hotel.Service(simpy.Resource(env, capacity= 10), 'facial_treatments', prm.fun,[hotel.Utility('facial_treatments', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 40)
body_treatments = hotel.Service(simpy.Resource(env, capacity= 10), 'body_treatments', prm.fun,[hotel.Utility('body_treatments', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 60)
heated_pool = hotel.Service(simpy.Resource(env, capacity= 10), 'heated_pool', prm.fun,[hotel.Utility('heated_pool', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 55)
jacuzzi = hotel.Service(simpy.Resource(env, capacity= 10), 'jacuzzi', prm.fun,[hotel.Utility('jacuzzi', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 95)
sauna = hotel.Service(simpy.Resource(env, capacity= 10), 'sauna', prm.fun,[hotel.Utility('sauna', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 40)
steam_room = hotel.Service(simpy.Resource(env, capacity= 10), 'steam_room', prm.comfort,[hotel.Utility('steam_room', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 30)
hair_salon = hotel.Service(simpy.Resource(env, capacity= 10), 'hair_salon', prm.comfort,[hotel.Utility('hair_salon', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 45)
yoga_service = hotel.Service(simpy.Resource(env, capacity= 10), 'yoga_service', prm.comfort,[hotel.Utility('yoga_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 71)
pilates_service = hotel.Service(simpy.Resource(env, capacity= 10), 'pilates_service', prm.comfort,[hotel.Utility('pilates_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 50)
reflexology_service = hotel.Service(simpy.Resource(env, capacity= 10), 'reflexology_service', prm.comfort,[hotel.Utility('reflexology_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 30)
aromatherapy_service = hotel.Service(simpy.Resource(env, capacity= 10), 'aromatheraphy_service', prm.energy,[hotel.Utility('aromatherapy_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 40)
turkish_baths = hotel.Service(simpy.Resource(env, capacity= 10), 'turkish_baths', prm.comfort,[hotel.Utility('turkish_bath', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 75)
beauty_treatments = hotel.Service(simpy.Resource(env, capacity= 10), 'beauty_treatments', prm.comfort,[hotel.Utility('beauty_treatments', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 90)
hair_removal_service = hotel.Service(simpy.Resource(env, capacity= 10), 'hair_removal_service', prm.comfort,[hotel.Utility('hair_removal_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 50)
library = hotel.Service(simpy.Resource(env, capacity= 10), 'library', prm.fun,[hotel.Utility('library', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 50)
game_room = hotel.Service(simpy.Resource(env, capacity= 10), 'game_room', prm.fun,[hotel.Utility('game_room', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 100)
bike_rental = hotel.Service(simpy.Resource(env, capacity= 10), 'bike_rental', prm.fun,[hotel.Utility('bike_rental', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 70)
car_rental = hotel.Service(simpy.Resource(env, capacity= 10), 'car_rental', prm.fun,[hotel.Utility('car_rental', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
motorcycle_rental = hotel.Service(simpy.Resource(env, capacity= 10), 'motorcycle_rental', prm.fun,[hotel.Utility('motorcycle_rental', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
live_music_service = hotel.Service(simpy.Resource(env, capacity= 10), 'live_music_service', prm.fun,[hotel.Utility('live_music_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 20)
karaoke = hotel.Service(simpy.Resource(env, capacity= 10), 'karaoke', prm.fun,[hotel.Utility('karaoke', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 45)
board_games = hotel.Service(simpy.Resource(env, capacity= 10), 'board_games', prm.fun,[hotel.Utility('board_games', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 37)
cinema = hotel.Service(simpy.Resource(env, capacity= 10), 'cinema', prm.fun,[hotel.Utility('cinema', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 90)
printing_service = hotel.Service(simpy.Resource(env, capacity= 10), 'printing_service', prm.comfort,[hotel.Utility('printing_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100), 50)
mail_service = hotel.Service(simpy.Resource(env, capacity= 10), 'mail_service', prm.comfort,[hotel.Utility('mail_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
currency_exchange_service = hotel.Service(simpy.Resource(env, capacity= 10), 'currency_exchange_service', prm.comfort,[hotel.Utility('currency_exchange_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
medical_assistance_service = hotel.Service(simpy.Resource(env, capacity= 10), 'medical_assistance_service', prm.comfort,[hotel.Utility('medical_assistance_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
sports_equipment_rental = hotel.Service(simpy.Resource(env, capacity= 10), 'sports_equipment_rental', prm.comfort,[hotel.Utility('sports_equipment_rental', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
flower_delivery_service = hotel.Service(simpy.Resource(env, capacity= 10), 'flower_delivery_service', prm.comfort,[hotel.Utility('flower_delivery_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
wedding_service = hotel.Service(simpy.Resource(env, capacity= 10), 'wedding_service', prm.comfort,[hotel.Utility('wedding_service', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
honeymoon_service = hotel.Service(simpy.Resource(env, capacity= 10), 'honeymoon', prm.fun,[hotel.Utility('honeymoon', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
romantic_dinner = hotel.Service(simpy.Resource(env, capacity= 10), 'romantic_dinner', prm.food,[hotel.Utility('romantic_dinner', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
shopping = hotel.Service(simpy.Resource(env, capacity= 10), 'shopping', prm.fun,[hotel.Utility('shopping', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
daycare = hotel.Service(simpy.Resource(env, capacity= 10), 'daycare', prm.comfort,[hotel.Utility('daycare', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
dive = hotel.Service(simpy.Resource(env, capacity= 10), 'dive', prm.fun,[hotel.Utility('dive', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
parachute = hotel.Service(simpy.Resource(env, capacity= 10), 'parachute', prm.fun,[hotel.Utility('parachute', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
dance_classes = hotel.Service(simpy.Resource(env, capacity= 10), 'dance_class', prm.fun,[hotel.Utility('dance_class', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
boat_rides = hotel.Service(simpy.Resource(env, capacity= 10), 'boat_rides', prm.fun,[hotel.Utility('boat_rides', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))
kayak_rental = hotel.Service(simpy.Resource(env, capacity= 10), 'kayak_rental', prm.fun,[hotel.Utility('kayak_rental', simpy.Container(env, prm.ROOM_CLEANING_SIZE, init= prm.ROOM_CLEANING_SIZE))], random.randint(20, 100))


services_ = [[rest_room], [pool], [coffee], [energy_drink], [buffet], [snack_bar], [room_service], [restaurant],[continental_breakfast, restaurant],[buffet_breakfast, restaurant], [carte_breakfast, restaurant],[carte_dinner, restaurant],[tasting_menu, restaurant],[ranchon], [pool_table], [table_tennis], 
            [tennis], [gym], [show_time], [ironing_service], [laundry_service], [wi_fi], [transfer_service], [excursion], [souvenir_shopping], [local_cuisine_restaurant], [International_cuisine_restaurant], [bar], [pool_bar], 
            [information_bureau], [spa], [masaje], [facial_treatments], [body_treatments], [heated_pool], [jacuzzi], [sauna], [steam_room], [hair_salon], [yoga_service],
            [pilates_service], [reflexology_service], [aromatherapy_service], [turkish_baths], [beauty_treatments], [hair_removal_service], [library], [game_room],
            [bike_rental], [car_rental], [motorcycle_rental], [live_music_service], [karaoke], [board_games], [cinema], [printing_service], [mail_service], [currency_exchange_service],
            [medical_assistance_service], [sports_equipment_rental], [flower_delivery_service], [wedding_service], [honeymoon_service], [romantic_dinner], [shopping],
            [daycare], [dive], [parachute], [dance_classes], [boat_rides], [kayak_rental]]
#Corrwgir utilidades
#[continental_breakfast, restaurant], [buffet_breakfast,restaurant], [carte_breakfast, restaurant], [carte_dinner, restaurant], [tasting_menu, restaurant]