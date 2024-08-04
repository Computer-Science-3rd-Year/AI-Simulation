import params as prm


# servicios que un turista en particular necesita para satisfacer sus necesidades
def beliefs(rooms): #agregar THRESHOLD_CLEAN por cada habiteichon
    dict_ = {} # {'room_1': [level_clean, availability], 'room_2': [level_clean, availability]}
    dict_['rooms'] = {}
    for room in rooms:
        dict_['rooms'][room] = [room.utilities[0].container.level, True]
    
    dict_['working'] = False
    
    return dict_

def desires(beliefs):
    dict_ = {} # {'room_1': availability, 'room_2': availability, ...}
    for room in beliefs['rooms']:
        dict_[room] = False
    return dict_

def brf(hotel, beliefs):
   for room in hotel.rooms.services:
       if room in beliefs['rooms']:
           beliefs[room] = [room.utilities[0].container.level, hotel.rooms.services[room]]

def generate_option(beliefs, desires):
    for room in beliefs['rooms']:
        if beliefs['rooms'][room][1]:
            #print((room.utilities.container.level / beliefs[room][0]) * 100, 'calculo')
            if  room.utilities[0].container.level < prm.THRESHOLD_CLEAN:
                desires[room] = True
                

    
def filter(desires):
    intentions = []
    for room in desires:
        if desires[room] and not room.using:
            intentions.append(room)
    return intentions

