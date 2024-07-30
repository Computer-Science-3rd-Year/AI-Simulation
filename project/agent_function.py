def brf(self, hotel):
        if self.type_ == 'tourist':
            for service in hotel.services:
                necesity = service.necesity
                name = service.name
                if not necesity in self.perception and hotel[service]:
                    self.perception[necesity] = {name}
                    continue
                if necesity in self.perception and not name in self.perception[necesity] and hotel[service]:
                    self.perception[necesity].update([name])
                    continue                
                if name in self.perception[necesity] and not hotel[service]:
                    self.perception[necesity].remouve(name)         
        
        if self.type_ == 'worker':
            self.beliefs = workers.brf(self.beliefs, self.perception)

        if self.type_ == 'manager':
            self.beliefs = manager.brf(self.beliefs, self.perception)
    