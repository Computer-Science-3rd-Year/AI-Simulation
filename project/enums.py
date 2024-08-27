from enum import Enum

class Necesity(Enum):
    energy = 1
    food = 2
    fun = 3
    comfort = 4

class Services_name(Enum):
    rest_room = 1
    pool = 2
    coffee = 3
    energy_drink = 4
    buffet = 5
    snack_bar = 6
    room_service = 7
    restaurant = 8
    ranchon = 9
    pool_table = 10
    table_tennis = 11
    tennis = 12
    gym = 13
    show_time = 14
    ###############################
    ironing_service = 15
    laundry_service = 16
    wi_fi = 17
    transfer_service = 18
    excursion = 19
    souvenir_shopping = 20
    continental_breakfast = 21
    buffet_breakfast = 22
    carte_breakfast = 23
    carte_dinner = 24
    tasting_menu = 25
    local_cuisine_restaurant = 26
    international_cuisine_restaurant = 27
    bar = 28
    pool_bar = 29
    information_bureau = 30
    spa = 31
    masaje = 32
    facial_treatments = 33
    body_treatments = 34
    heated_pool = 35
    jacuzzi = 36
    sauna = 37
    steam_room = 38
    hair_salon = 39
    yoga_service = 40
    pilates_service = 41
    reflexology_service = 42
    aromatherapy_service = 43
    turkish_baths = 44
    beauty_treatments = 45
    hair_removal_service = 46
    library = 47
    game_room = 48
    bike_rental = 49
    car_rental = 50
    motorcycle_rental = 51
    live_music_service = 52
    karaoke = 53
    board_games = 54
    cinema = 55
    printing_service = 56
    mail_service = 57
    currency_exchange_service = 58
    medical_assistance_service = 59
    sports_equipment_rental = 60
    flower_delivery_service = 61
    wedding_service = 62
    honeymoon_service = 63
    romantic_dinner = 64
    shopping = 65
    daycare = 66
    dive = 67
    parachute = 68
    dance_classes = 69
    boat_rides = 70
    kayak_rental = 71

class Satisfaction_classif(Enum):
    very_bad = 0
    bad = 1
    good = 2
    very_good = 3 
    excellent = 4
