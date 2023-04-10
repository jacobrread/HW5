import Objects
import random
import numpy as np
import matplotlib.pyplot as plt

def Main(args):
    # Check for valid command line arguments
    if len(args) != 1:
        print("Usage: python Game.py <strategy>")
        print("Available strategies are 'Dove' and 'Hawk'")
        return
    
    strategy = args[0]
    creatures = InitializeCreatures(strategy)
    # Check for valid strategy
    if creatures == None:
        print("Invalid strategy. Available strategies are 'Dove' and 'Hawk'")
        return
    
    num_food = 40
    totalDoves = []
    totalHawks = []

    # Game loop
    for i in range(0, 100):
        foodLocations = InitializeFood(num_food)

        # Place creatures
        for creature in creatures:
            placed = PlaceCreature(creature, foodLocations, num_food)
            if not placed:
                creature.is_alive = False

        # Determine creatures status
        for location in foodLocations:
            residents = location.GetCreatures()
            UpdateCreatures(residents)

        # Reproduce
        for creature in creatures:
            if random.random() < creature.change_to_reproduce:
                new_creature = Objects.Creature(creature.type)
                creatures.append(new_creature)
            
        # Update creatures list
        alive_creatures = []
        for creature in creatures:
            if creature.is_alive:
                alive_creatures.append(creature)

        doves = 0
        hawks = 0
        for creature in alive_creatures:
            if creature.type == "Dove":
                doves += 1
            else:
                hawks += 1

        totalDoves.append(doves)
        totalHawks.append(hawks)
    
    # Graph results
    plt.plot(totalDoves)
    plt.plot(totalHawks)
    plt.ylabel('Number of Creatures')
    plt.xlabel('Generation')
    plt.show()


# Updates the creatures based on their type
def UpdateCreatures(residents):
    if len(residents) == 0:
        return
    
    if len(residents) == 2:
        if residents[0].type == "Dove" and residents[1].type == "Hawk":
            residents[0].is_alive = False
            residents[0].change_to_reproduce = 0.0
            residents[1].is_alive = True
            residents[1].change_to_reproduce = 0.5
        elif residents[0].type == "Hawk" and residents[1].type == "Dove":
            residents[0].is_alive = True
            residents[0].change_to_reproduce = 0.5
            residents[1].is_alive = False
            residents[1].change_to_reproduce = 0.0
        elif residents[0].type == "Hawk" and residents[1].type == "Hawk":
            if residents[0].kills > residents[1].kills:
                residents[0].is_alive = True
                residents[0].change_to_reproduce = 0.5
                residents[1].kills += 1
                residents[1].is_alive = False
                residents[1].change_to_reproduce = 0.0
            elif residents[0].kills < residents[1].kills:
                residents[0].is_alive = False
                residents[0].change_to_reproduce = 0.0
                residents[1].is_alive = True
                residents[1].change_to_reproduce = 0.5
                residents[1].kills += 1
            else:
                residents[0].is_alive = False
                residents[0].change_to_reproduce = 0.0
                residents[1].is_alive = False
                residents[1].change_to_reproduce = 0.0
        else:
            residents[0].is_alive = True
            residents[0].change_to_reproduce = 0.0
            residents[1].is_alive = True
            residents[1].change_to_reproduce = 0.0

    if len(residents) == 1:
        residents[0].is_alive = True
        residents[0].change_to_reproduce = 1.0


# Recursively places a creature in a random location
# Returns True if the creature was placed, False if the map is full
def PlaceCreature(creature, foodLocations, num_food):
    # Check if there is any food left
    for foodLocation in foodLocations:
        if foodLocation.HasAvailableFood():
            break
        else:
            return False

    location = random.randint(0, num_food - 1)
    # If the location has food, update the creature. Otherwise, try again
    if (foodLocations[location].HasAvailableFood()):
        foodLocations[location].Update(creature)
    else:
        return PlaceCreature(creature, foodLocations, num_food)

    return True


# Populates the food array with the given number of food items
# Returns the food array
def InitializeFood(total_food):
    food = []
    for i in range(0, total_food):
        food.append(Objects.FoodLocation())

    return food


# Populates the creatures array based on the given strategy
# Returns the creatures array
def InitializeCreatures(strategy):
    creatures = []

    if strategy == "Dove":
        for i in range(0, 6):
            creature =  Objects.Creature("Dove")
            creatures.append(creature)
    elif strategy == "Hawk":
        for i in range(0, 5):
            creature =  Objects.Creature("Dove")
            creatures.append(creature)
        creatures.append(Objects.Creature("Hawk"))
    else:
        return None

    return creatures

    
# Main(["Dove"])
Main(["Hawk"])