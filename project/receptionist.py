import copy
import params as prm

def rooms_distributions(ordenated_tourist, count, dict, time, hotel, reserved_time):
    if count == len(ordenated_tourist):
        return dict
    
    else:
        restrictions = ordenated_tourist[count][1]['restrictions']
        for room in hotel.rooms.services:
            if room in reserved_time and time < reserved_time[room]:
                continue
            if not validate(restrictions, room):
                continue
            old_copy = copy.copy(dict)
            if room in reserved_time:
                old_time = reserved_time[room]
            else:
                old_time = prm.SIM_TIME + 400
            
            reserved_time[room] = time + ordenated_tourist[count][2]
            dict[ordenated_tourist[count][0]] = room
            result = rooms_distributions(ordenated_tourist, count + 1, dict, time, hotel, reserved_time)
            if result != None:
                return result
            dict = old_copy
            reserved_time[room] = old_time
        dict[ordenated_tourist[count][0]] = None
        return rooms_distributions(ordenated_tourist, count + 1, dict, time, hotel, reserved_time)

def validate(restrictions, room):
    for item in restrictions:
        if item not in room.attributes:
            return False
    return True
  
def bad_room(dict, hotel, time, ordenated_tourist, reserved_time):
    for item in ordenated_tourist:
        if dict[item[0]] == None:
            for room in hotel.rooms.services:
                if room in reserved_time and time < reserved_time[room]:
                    continue
                reserved_time[room] = time + item[2]
                dict[item[0]] = room
                break
           
