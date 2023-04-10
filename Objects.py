# FoodLocation Object
class FoodLocation:
    def __init__(self):
        self.food1 = None
        self.food2 = None

    def Update(self, food):
        if self.food1 == None:
            self.food1 = food
        elif self.food2 == None:
            self.food2 = food
    
    def HasAvailableFood(self):
        return self.food1 == None or self.food2 == None
    
    def GetCreatures(self):
        creatures = []
        if self.food1 != None:
            creatures.append(self.food1)
        if self.food2 != None:
            creatures.append(self.food2)
        return creatures

    

# Creature Object
class Creature:
    def __init__(self, type):
        self.type = type
        self.change_to_reproduce = 0.0
        self.is_alive = True
        self.kills = 0