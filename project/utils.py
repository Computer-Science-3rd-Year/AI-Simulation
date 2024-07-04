import simpy

class My_container(simpy.Container):
    def __init__(self, env, name: str, capacity: int | float = ..., init: int | float = 0):
        super().__init__(env, capacity, init)
        self.name = name


class My_resource(simpy.Resource):
    def __init__(self, env, name: str, container: My_container=None, capacity: int = 1):
        super().__init__(env, capacity)
        self.name = name
        self.container = container