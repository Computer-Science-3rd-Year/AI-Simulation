import simpy 
import tourists
import workers
import manager

class AGENT: # Agente BDI --> todas las funciones/componentes 
    def __init__(self, name, beliefs, desires, intentions, type):
        self.name = name
        self.beliefs = beliefs # {'perceptions': ..., 'rules': ...}
        self.desires = desires
        self.intentions = intentions
        self.type = type
        self.perception = None # propiedades de Hotel en dependencia del tipo de agente y coincide con la estructura respectiva en Hotel
        self.location = None
    
    
    def brf(self, hotel):
        if self.beliefs[0] in tourists.beliefs:
            for service in hotel.services:
                if not service in self.perception and hotel[service]:
                    self.perception[service] = True
                    continue
                if service in self.perception and not hotel[service]:
                    del self.perception[service]            
        
        if self.beliefs[0] in workers.beliefs:
            self.beliefs = workers.brf(self.beliefs, self.perception)

        if self.beliefs[0] in manager.beliefs:
            self.beliefs = manager.brf(self.beliefs, self.perception)
            
        

    def generate_options(self):
        if self.beliefs[0] in tourists.beliefs:
            self.desires = tourists.generate_option(self.beliefs, self.intentions)          
            return
        
        if self.beliefs[0] in workers.beliefs:
            self.desires = workers.generate_option(self.beliefs, self.intentions)          
            return
        
        if self.beliefs[0] in manager.beliefs:
            self.desires = manager.generate_option(self.beliefs, self.intentions)

    # NO ADD nuevas intenciones
    def filter(self):
        if self.beliefs[0] in tourists.beliefs:
            self.intentions = tourists.filter(self.beliefs, self.desires, self.intentions)          
            return
        
        if self.beliefs[0] in workers.beliefs:
            self.intentions = workers.filter(self.beliefs, self.desires, self.intentions)          
            return
        
        if self.beliefs[0] in manager.beliefs:
            self.intentions = manager.filter(self.beliefs, self.desires, self.intentions)

    
    def action(self):
        self.brf()
        self.generate_options()
        self.filter()
        return self.intentions[0] # intención de mayor prioridad




# DxP-->D dtoma una base de datos (interna del agente) y una percepción y devuelve una base de datos (interna del agente)
def next(): # ver def de next a partir de old y new en LT pág 65
    pass
# E-->R asigna un valor real a cada estado del ambiente (cuán útil es un estado para un agente)
def utility():
    pass
def rule(): # reglas de deducción (unificar como PROLOG según LT) ver LT pág 65
    pass
# ganma --> índice de cambio del ambiente: a mayor índice => agente_más_precavido

# ganma(Bel)xP-->ganma(Bel) dada una percepción y un conjunto de beliefs determina un nuevo conjunto de beliefs
def brf(perception): # todo lo que el agente observa del medio 
                            # perception --> [hotel.property_1, hotel.property_2, ..., hotel.property_3]
                            # cada perception varia de acuerdo con la inst de agente => se usará una func lambda para generarlas
    new_beliefs = agent.beliefs
    for bel in agent.beliefs:
        pass
    return new_beliefs

# ganma(Bel)xganma(Int)-->ganma(Des) dado un conjunto de beliefs y un conjunto de intentions devuelve un conjunto de desires
# proceso de PLANIFICACION del agente (lograr las intenciones del agente)
# elaboración recursiva de estructuras de planes jerárquicos
# considera y realiza intenciones cada vez más específicas hasta que se corresponda con una acción inmediata
# CONSISTENCIA: las opciones deben ser consistentes con las creencias y las intenciones actuales
# OPORTUNISMO: verificar los cambios del ambiente para detectar nuevas condiciones favorables
def generate_options(self): 
    new_desires = agent.desires
    for bel in agent.beliefs:
        for int in agent.intentions:
            pass
    return new_desires
# ganma(Bel)xganma(Int)xganma(Des)-->ganma(Int)
# dado un conjunto de beliefs, intentions y desires devuelve un conjunto de intentions
# proceso de DELIBERACION del agente (ajustar frecuencia según dinamismo del ambiente)
# ACTUALIZAR eliminar intenciones inválidas o cuyo costo supere la ganancia
# MANTENER intenciones no logradas con beneficio positivo
# NO ADD nuevas intenciones
def filter(self):
    new_intentions = agent.intentions
    for bel in agent.beliefs:
        for des in agent.desires:
            for int in agent.intentions:
                pass
    return new_intentions
# P*-->A dada una secuencia de percepciones las transforma en una acción
# I-->A des estados internos en acciones (pues será un agente con estados)
# D-->A (para agentes inteligentes) de una base de datos (interna del agente) devuelve una acción
def action(self): # lo que el agente hace con el medio, a partir de lo que observa
    self.brf()
    self.generate_options()
    self.filter()
    return self.intentions[0] # intención de mayor prioridad
