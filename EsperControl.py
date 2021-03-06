###########################################################################
##Creator: Cole Miller
##This Entity-Component System is a modified version of the Esper module
##Links
##https://docs.python.org/3/library/dataclasses.html#module-dataclasses
##https://github.com/benmoran56/esper/blob/master/esper/__init__.py
###########################################################################
try: 
    import pygame
    from pygame.locals import *
    from pygame.math import Vector2
    import sys
    from dataclasses import dataclass as component
    import time

    #My modules
    import Color

except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

class BaseSystem:
    priority = 0    #0 is the lowest priority

    def update(self, EM, *args, **kwargs):
        raise NotImplementedError

class testingSystem(BaseSystem):
    def update(self, EM, UI):
        x = 0
        while x != 100:
            x += 1

class testingSystemTwo(BaseSystem):
    def update(self, EM, UI):
        pass

@component
class testingComponentOne():
    x: int = 0

@component
class testingComponentTwo():
    y: int = 1

#Entity
class entityManager:
    def __init__(self):
        self.systems = []
        self.nextEntityID = 0
        self.components = {}
        self.entities = {}
        self.dyingEntities = set()
        self.updateTimesinNanoSeconds = {}
        
    def removeAllEntitiesAndComponents(self):
        self.nextEntityID = 0
        
        self.dyingEntities.clear()
        self.entities.clear()
        self.components.clear()
        
    def removeAllComponents(self, entity):
        for componentType in self.entities[entity]:
                self.components[componentType].discard(entity)

    def removeDyingEntities(self):
        for dyingEntity in self.dyingEntities:   
            self.removeAllComponents(dyingEntity)
            del self.entities[dyingEntity]
        
        self.dyingEntities.clear()
        
    def addSystem(self, system, priority):
        assert issubclass(system.__class__, BaseSystem)

        gotSystem = self.getSystem(system)
        
        if gotSystem == None:
            self.systems.append(system)
            lastItemInList = -1
            self.systems[lastItemInList].priority = priority
        
        else:
            #Overwrite current system's priority
            indexLocation = self.systems.index(gotSystem)
            self.systems[indexLocation].priority = priority

        #0 = lowest priority, higher priority systems will be moved to the front of the list
        self.systems.sort(key = lambda object: object.priority, reverse = True)
        
    def removeSystem(self, system):
        try:
            self.systems.remove(system)
        except:
            #System does not exist or has been removed previously
            pass
 
    def getSystem(self, sys):
        gotSystem = None
        for system in self.systems:
            if isinstance(system, type(sys)):
                gotSystem = system
            else:
                gotSystem = None

        return gotSystem
    
    def errorUpdatingSystem(self, system):
        print("Error updating system ", end="")
        print(system)

    def updateSystems(self, *args, **kwargs):
        for system in self.systems:
            try:
                system.update(self, *args, **kwargs)
            except:
                self.errorUpdatingSystem(system)

    def timedUpdateSystems(self, *args, **kwargs):
        for system in self.systems:
            try:
                startTime = time.process_time_ns()

                system.update(*args, **kwargs)

                timeBetweenCalls = (time.process_time_ns() - startTime)
                self.updateTimesinNanoSeconds[system] = timeBetweenCalls
            except:
                self.errorUpdatingSystem(system)

    def addEntity(self, *components):
        self.nextEntityID += 1
        
        self.entities[self.nextEntityID] = {}

        #Optional way to add components to the Entity when it is created
        for component in components:
            self.addComponent(self.nextEntityID, component)
        
        return self.nextEntityID
        
    def setupDyingEntity(self, entity):
        self.dyingEntities.add(entity)
    
    def entityExists(self, entityToFind):
        gotEntity = None
        for EntityID in self.entities.keys():
            if entityToFind == EntityID:
                gotEntity = EntityID
            else:
                gotEntity = None

        return gotEntity
        
    def addComponent(self, entity, component):
        componentType = type(component)

        if componentType not in self.components:
            self.components[componentType] = set()

        #Store the entity's ID in a Set for that component e.g. Position component has {1, 2} meaning both Entity 1 and 2 have this component
        self.components[componentType].add(entity)

        self.entities[entity][componentType] = component
        
    def removeComponent(self, entity, component):
        componentType = type(component)
        try:
            self.components[componentType].discard(entity)

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
        
    def getComponents(self, entity, *components):
        gotComponents = []
        for comp in components:
            gotComponent = self.getComponent(entity, comp)

            if gotComponent != None:
                gotComponents.append(gotComponent)

        return gotComponents

    #Entities and Components are tightly coupled so they will be tested together
    def testEntityAndComponents(self):
        #creation
        testEntityOne = self.addEntity()
        testingComponentOneOne = testingComponentOne()
        self.addComponent(testEntityOne, testingComponentOneOne)

        #overwriting components
        testingComponentOneOne = testingComponentOne(1)
        self.addComponent(testEntityOne, testingComponentOneOne)

        testEntityTwo = self.addEntity()
        self.addComponent(testEntityTwo, testingComponentOneOne)

        self.addEntity(testingComponentOne(), testingComponentTwo())

        self.entityExists(testEntityTwo)

        nonExistentEntity = -1
        self.entityExists(nonExistentEntity)

        self.getComponent(testEntityOne, testingComponentOneOne)

        self.getComponents(testEntityOne, testingComponentOne(), testingComponentTwo())
        self.addComponent(testEntityOne, testingComponentTwo())
        self.getComponents(testEntityOne, testingComponentOne(), testingComponentTwo())

        self.removeComponent(testEntityOne, testingComponentTwo())

        self.setupDyingEntity(testEntityTwo)
        self.removeDyingEntities()

        self.entityExists(testEntityTwo)

        self.removeAllEntitiesAndComponents()
        
    def testSystem(self):
        testSystem = testingSystem()
        priortity = 0
        self.addSystem(testSystem, priortity)

        #Check overwriting
        priortity = 1
        self.addSystem(testSystem, priortity)

        priortity = 2
        testSystemTwo = testingSystemTwo()
        self.addSystem(testSystemTwo, priortity)

        self.getSystem(testSystem)

        self.updateSystems()

        self.timedUpdateSystems()

        self.removeSystem(testSystem)
        #Check removing a system that does not exist in the systems list
        self.removeSystem(testSystem)

    def testSuiteForEntityManager(self):
        #Include all test functions here
        self.testSystem()  
        self.testEntityAndComponents()	
        self.debugPrint()

    def debugPrint(self):
        print("Entities: ", end="")
        print(self.entities)

        print("Components: ", end="")
        print(self.components)

        print("Dying Entities: ", end="")
        print(self.dyingEntities)

        print("Systems: ", end="")
        print(self.systems)

        print("Update Times (in nanoseconds): ", end="")
        print(self.updateTimesinNanoSeconds)

########            Testing         ###############
#EM = entityManager()
#EM.testSuiteForEntityManager()

#Changing an Entity's Components variables
#EnemyOne = EM.addEntity(testingComponentOne(), testingComponentTwo())
#EM.getComponent(EnemyOne, testingComponentTwo()).y = 50

#or
#tempComponent = EM.getComponent(EnemyOne, testingComponentTwo())
#tempComponent.y = 3
#print(EM.entities)


#New additions for the game 
@component
class Position():
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

@component
class Velocity():
    xVelocity: int = 0
    yVelocity: int = 0

@component
class Renderable():
    def __init__(self, height = 50, width = 50, color = (255,255,0)):
        #image:
        self.color = color  
        self.height = height
        self.width = width

@component
class Health():
    hp: int = 1

@component
class Score():
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    score: int = 0

@component
class Inventory():
    #inventory: list = []
    gold: int = 0

@component
class Attack():
    atkDamage: int = 1
    atkDamageModifier = 1
    atkRange: int = 2
    atkDamageType: str = "Normal"

class combatSystem(BaseSystem):
    def update(self):
        pass
        #for each entity that "attacked" this turn/frame and has the attack and health component
            #handle attack

class movementSystem(BaseSystem):
    def update(self):
        pass
        #for each entity with position and velocity
            #modify position
            #check collisions
            #finalize position

class renderSystem(BaseSystem):
    def update(self, EM, UI):
        self.ui = UI
        #print(EM.components)
        print(EM.components[Position])
        for entity in EM.entities:
            posComp = EM.getComponent(entity, Position())
            rendComp = EM.getComponent(entity, Renderable())
            if posComp != None and rendComp != None:
                #print("Render Entity")
                entityRect = pygame.Rect((posComp.x, posComp.y, rendComp.width, rendComp.height))
                
                #UI.window.blit(entityRect, UI.window)
                self.ui.window.fill(Color.white)
