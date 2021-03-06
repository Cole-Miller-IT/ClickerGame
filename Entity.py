#https://github.com/benmoran56/esper/blob/master/esper/__init__.py
from dataclasses import dataclass as component

#Base system class
class System:
    priority = 0

    def process(self, *args, **kwargs):
        raise NotImplementedError

class testingSystem(System):
    def __init__(self):
        super().__init__()

    def process(self):
        pass
            
class movementSystem(System):
    def __init__(self):
        super().__init__()
        
    def process(self):
        pass
        #for entity, (mov, pos) in self.entityManager.getComponents(Movement, Position):
        #    pos.y += mov

#Entity
class entityManager:
    def __init__(self):
        self.systems = []
        self.nextEntityID = 0
        self.components = {}
        self.entities = {}
        self.dyingEntities = set()
        self.getComponentCache = {}
        self.getComponentsCache = {}
        
    def clearAllComponents(self):
        self.getComponentCache = {}
        self.getComponentsCache = {}
        
    def clearAllEntitiesAndComponents(self):
        self.nextEntityID = 0
        
        self.dyingEntities.clear()
        self.components.clear()
        self.entities.clear()
        self.clearAllComponents()
        
    def clearDyingEntities(self):
        for dyingEntity in self.dyingEntities:
            for component in self.entities[dyingEntity]:
                self.components[component].discard(dyingEntity)
                
            del self.entities[dyingEntity]
        
        self.dyingEntities.clear()
        self.clearAllComponents()
        
    def addSystem(self, system, priority):
        assert issubclass(system, System)
        
        system.priority = priority
        
        self.systems.append(system)
        
        #0 = lowest priority
        self.systems.sort(key = lambda prioritySort: system.priority, reverse = True)
        
    def removeSystem(self, system):
        self.systems.remove(system)
        
    def getSystem(self, sys):
        for system in self.systems:
            if isinstance(sys, system):
                return sys
                
        else:
            return None
    
    def updateSystems(self, *args, **kwargs):
        for system in self.systems:
            system.process(self, *args, **kwargs)
                
    def addEntity(self, *components):
        self.nextEntityID += 1
        
        for component in components:
            self.addComponent(self.nextEntityID, component)
        
        return self.nextEntityID
        
    def setupDyingEntity(self, entity):
        self.dyingEntities.add(entity)
        
    def entityExists(self):
        pass
        
    def retrieveEntityComponent(self):
        pass
        
    def retrieveEntityComponents(self):
        pass
        
    def hasComponent(self):
        pass
        
    def hasComponents(self):
        pass

    #Testing This  
    def addComponent(self, entity, component):
        self.components.update(entity)

        if entity not in self.entities:
            self.entities[entity] = {}

        #self.entities[entity][]
        self.clearAllComponents()
        
    def removeComponent(self):
        pass
    
    def getComponent(self):
        pass
        
    def getComponents(self):
        pass
      
    def testSuiteForEntityManager(self):
        #Include all test functions here
        self.testSystem()
    
    def testSystem(self):
        testSystem = testingSystem
        priority = 1
        self.addSystem(testSystem, priority)
        self.getSystem(testSystem)
        self.updateSystems()
        self.removeSystem(testSystem)

    def testEntity(self):
        self.addEntity(Testing())
        print(self.entities)
		
##########################################
#https://docs.python.org/3/library/dataclasses.html#module-dataclasses
#Components, built using the dataclasses library


@component
class Testing:
    x: float = 0.0
    y: float = 0.0

@component
class Position:
    x: float = 0.0
    y: float = 0.0
   
@component   
class Movement:
    movespeedPerSecond: int = 20
    
#Testing
EM = entityManager()
EM.testSystem()
EM.testEntity()