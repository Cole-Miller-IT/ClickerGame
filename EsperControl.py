##########################################
#https://docs.python.org/3/library/dataclasses.html#module-dataclasses
#Components, built using the dataclasses library
#https://github.com/benmoran56/esper/blob/master/esper/__init__.py
from dataclasses import dataclass as component

class System:
    priority = 0

    def process(self, *args, **kwargs):
        raise NotImplementedError

class testingSystem(System):
    def process(self):
        pass
            
class movementSystem(System):
    def process(self):
        pass
        #for entity, (mov, pos) in self.entityManager.getComponents(Movement, Position):
        #    pos.y += mov


@component
class Testing:
    x: int = 0

@component
class Position:
    x: float = 0.0
    y: float = 0.0
   
@component   
class Movement:
    movespeedPerSecond: int = 20


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
            if isinstance(sys, System):
                return sys
                
            else:
                return None
    
    def updateSystems(self, *args, **kwargs):
        for system in self.systems:
            system.process(*args, **kwargs)
                
    def addEntity(self, *components):
        self.nextEntityID += 1
        
        self.entities[self.nextEntityID] = {}

        #for component in components:
            #self.addComponent(self.nextEntityID, component)
        
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
        
    def addComponent(self, entity, component):
        componentType = type(component)
        print(componentType)
        print(self.entities[entity])
        self.entities[entity][componentType] = component
        print(self.entities[entity][componentType])
        
        
    def removeComponent(self, entity, component):
        componentType = type(component)
        try:
            del self.entities[entity][componentType]
        except:
            print("Entity has no component to remove")

        return entity
    
    def getComponent(self, entity, component):
        componentType = type(component)
        entitiesComponents = self.entities.get(entity)
        specificComponent = entitiesComponents.get(componentType)

        #Returns None if the entity does not have the component
        return specificComponent
        
    def getComponents(self):
        pass

    def testComponentMethods(self):
        testEntity = 1

        self.addComponent(testEntity, Testing())
        self.addComponent(testEntity, Testing())
        self.getComponent(testEntity, Testing())
        self.removeComponent(testEntity, Testing())
        self.getComponent(testEntity, Testing())
        self.removeComponent(testEntity, Testing())
      
    def testSuiteForEntityManager(self):
        #Include all test functions here
        self.testSystem()
    
    def testSystem(self):
        testSystem = testingSystem()
        priortity = 0

        self.addSystem(testSystem, priortity)
        print(self.systems)

        self.addSystem(testSystem, 1)
        self.addSystem(testSystem, 1)
        self.addSystem(testSystem, 2)
        print(self.systems)
        for system in self.systems:
            print(system.priority)

        x = self.getSystem(testSystem)
        print(x)

        self.updateSystems()

        self.removeSystem(testSystem)
        print(self.systems)
		