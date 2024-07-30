class Tourist:
    def __init__(self, hotel):
        self.access = []
        self.init_access(hotel)
    
    def init_access(self, hotel):
        for serv in hotel.services:
            self.access.append(serv[0])
