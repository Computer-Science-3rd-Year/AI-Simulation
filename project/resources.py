# import simpy

# class Room(simpy.Resource):
#     def __init__(self, env, num_rooms=10):
#         super().__init__(env, capacity=num_rooms)
        
    
#     # add proceso de dormir/estar en la habitación (esto se hace al revés:  al proceso se le asocia un recurso sobre el cual proceder)

# class Reception(simpy.Resource):
#     def __init__(self, env, num_serv=1):
#         super().__init__(env)
#         self.num_serv = num_serv
    
#     # add algo con colas, asociarle un trabajador
