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

def execute_action(env, rooms, hotel, beliefs, outputs):
        #print('housemaiddddddddddd')
        if rooms == []:
            return       
        for room in rooms:
            beliefs['working'] = True
            with room.resource.request() as rq: 
                room.using = True
                yield rq
                #print(f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities.name} of the {room.name}...')-----------------------------
                bed = room.utilities[0].container
                #print(bed.capacity, bed.level)
                amount = bed.capacity - bed.level
                #print(f'total: {bed.capacity}, level: {bed.level}, {room.name}')
                if amount == 0: return # PARCHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                outputs.append((env.now, f'{env.now:6.1f} s: Housemaid is cleaning the {room.utilities[0].name} of the {room.name}...'))
                hotel.revenues[room] -= room.worker[1]
                hotel.budget -= room.worker[1]
                outputs.append((env.now, f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}'))
                #print(f'{env.now:6.1f} s: Level before clean the {room.name}: {bed.level}')---------------------------------------
                
                bed.put(amount)
                #outputs.append((env.now,(room.name, bed.level)))
                
                
                yield env.timeout(prm.HOUSEMAID_TIME)
                #outputs.append((env.now, (room.name, bed.level, 'bbbbbbbbbbbbbbbbbbb')))
                room.using = False
                beliefs['working'] = False
                outputs.append((env.now, f'{env.now:6.1f} s: Housemaid finished and the {room.name} is clean'))
                outputs.append((env.now, f'Level after clean {room.name}: {bed.level}'))
