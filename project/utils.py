import params as prm


def Lower_raise_salary(hotel, operator):
    for room in hotel.rooms.services:
        if operator:
            room.worker[1] += room.worker[1]/10
        else:
            room.worker[1] -= room.worker[1]/10
    for service in hotel.services:
        if operator:
            service.worker[1] += service.worker[1]/10
        else:
            service.worker[1] += service.worker[1]/10
    if operator:
        prm.HOUSEMAID_TIME -= 1
        prm.HOUSEMAID_TIME = max(3, prm.HOUSEMAID_TIME)
    else:
        prm.HOUSEMAID_TIME += 1

def occupate_rooms(hotel):
    count = 0
    for room in hotel.rooms.services:
        if room.resource.count == 0:
            continue
        count += 1
    return count/len(hotel.rooms.services)

def calculate_service(hotel, operator):
    if operator:
        max_revenue = 0
    else:
        max_revenue = 1000000000000
    service_return = None
    for service in hotel.revenues:
        if not service in hotel.rooms.services and hotel.services[service]:
            value = hotel.revenues[service]
            cost = hotel.expenses_of_service(service)
            if value - cost >= max_revenue and operator:
                max_revenue = value - cost
                service_return = service
            if value - cost <= max_revenue and not operator:
                max_revenue = value - cost
                service_return = service
    return service_return

def check(service, hotel):
    necesity_ = service.necesity
    count = 0
    for serv in hotel.services:
        if serv.necesity == necesity_ and hotel.services[service]:
            count += 1    
    return count > 1

def AI_function_services(hotel, services_, test):
    combinations = []
    if test:
        a = combination(services_, [], 200, 0, hotel, combinations)
    else:
        a = combination_iter(services_, [], 200, 0, hotel, [], [0,0])
    return a

def combination(services_, combination_, budget, minor, hotel, combinations):
    if budget <= 20:
        total = 0
        for i in combination_:
            if len(i) == 1:
                total += i[0].price
            else:
                total += i[1].price/5
        if total > 250:
            return combination_
        else:
            return None
    else:
        for i in range(minor, len(services_)):
            k = len(combination_)
            if services_[i][0] not in hotel.services or not hotel.services[services_[i][0]] or (len(services_[i]) > 1 and ((services_[i][1] in hotel.services and hotel.services[services_[i][1]]) or services_[i][1] in combination_)):
                combination_.append(services_[i])
                if len(services_[i]) == 1:
                    new_budget = budget - services_[i][0].cost
                else:
                    new_budget = budget - (services_[i][1].cost/5)
                result = combination(services_, combination_, new_budget, i + 1, hotel, combinations)
                if result != None:
                    return result
                combination_ = combination_[:k]

def combination_iter(services_, combination_, budget, minor, hotel, best_combination, best_amount):
    if budget <= 20:
        total = 0
        aux = []
        for i in combination_:
            if len(i) == 1:
                total += i[0].price
                aux.append([i[0]])
            else:
                total += i[1].price/5
                aux.append([i[0], i[1]])
        if total > best_amount[0]:
            best_amount[0] = total
            best_combination.append(aux)
            
        best_amount[1] += 1

        if best_amount[1] == 100000:
            return best_combination[-1]
        return None
    else:
        for i in range(minor, len(services_)):
            k = len(combination_)
            if services_[i][0] not in hotel.services or not hotel.services[services_[i][0]] or (len(services_[i]) > 1 and ((services_[i][1] in hotel.services and hotel.services[services_[i][1]]) or services_[i][1] in combination_)):
                combination_.append(services_[i])
                if len(services_[i]) == 1:
                    new_budget = budget - services_[i][0].cost
                else:
                    new_budget = budget - (services_[i][1].cost/5)
                result = combination_iter(services_, combination_, new_budget, i + 1, hotel, best_combination, best_amount)
                if result != None:
                    return result
                combination_ = combination_[:k]
