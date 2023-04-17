import Objects
import random
import numpy as np
import matplotlib.pyplot as plt
import sys
import multiprocessing
from joblib import Parallel, delayed

def Main(args):
    # Check for valid command line arguments
    if len(args) != 3:
        print("Usage: python Game.py <strategy> <version>")
        print("Available strategies are 'Dove' and 'Hawk'")
        print("Available versions are 'Vanilla' and 'Modified'")
        return
    
    strategy = args[1]
    version = args[2]
    creatures = InitializeCreatures(strategy)
    # Check for valid strategy
    if creatures == None:
        print("Invalid strategy. Available strategies are 'Dove' and 'Hawk'")
        return
    
    num_food = 40
    iterations = 100
    totalDoves = []
    totalHawks = []

    # Game loop
    if version == 'Vanilla':
        totalDoves, totalHawks = VanillaGameLoop(creatures, num_food, iterations)
    else:
        totalDoves, totalHawks = ModifiedGameLoop(creatures, num_food, iterations)
    
    # Graph results
    plt.plot(totalDoves)
    if strategy == 'Hawk':
        plt.plot(totalHawks)
    plt.ylabel('Number of Creatures')
    plt.xlabel('Generation')
    plt.show()

    # Print stats to the console
    print("Strategy: " + strategy)
    print("Version: " + version)
    print("Total doves: " + str(totalDoves[-1]))
    print("Total hawks: " + str(totalHawks[-1]))
    print("Average doves: " + str(np.mean(totalDoves)))
    print("Average hawks: " + str(np.mean(totalHawks)))
    print()


# Method to collect a lot of data
def CollectData():
    runs = [["Dove", "Vanilla"],
            ["Dove", "Modified"],
            ["Hawk", "Vanilla"],
            ["Hawk", "Modified"]]
    
    results = []

    if __name__ == '__main__':
        pool = multiprocessing.Pool()           
        results = pool.map(MyFunction, runs)
        pool.close()
        pool.join()

    # graph results
    for i in range(0, len(runs)):
        run = runs[i]
        result = results[i]
        overallTotalDoves = result[0]
        overallTotalHawks = result[1]

        # Graph results
        plt.plot(overallTotalDoves)
        if run[0] == 'Hawk':
            plt.plot(overallTotalHawks)
        plt.ylabel('Number of Creatures')
        plt.xlabel('Generation')
        plt.show()

        # Print stats to the console
        print("Strategy: " + run[0])
        print("Version: " + run[1])
        print("Total doves: " + str(overallTotalDoves[-1]))
        print("Total hawks: " + str(overallTotalHawks[-1]))
        print("Average doves: " + str(np.mean(overallTotalDoves)))
        print("Average hawks: " + str(np.mean(overallTotalHawks)))
        print()


# Function to run in parallel
def MyFunction(run):
    strategy = run[0]
    version = run[1]
    creatures = InitializeCreatures(strategy)

    num_food = 40
    iterations = 100
    experiments = 1

    runTotalDoves = []
    runTotalHawks = []
    
    # run each experiment n times
    for i in range(0, experiments):
        totalDoves = []
        totalHawks = []
        # Game loop
        if version == 'Vanilla':
            totalDoves, totalHawks = VanillaGameLoop(creatures, num_food, iterations)
        else:
            totalDoves, totalHawks = ModifiedGameLoop(creatures, num_food, iterations)

        runTotalDoves.append(totalDoves)
        runTotalHawks.append(totalHawks)
    
    return runTotalDoves, runTotalHawks


# Runs the game as explained in the video
# Returns the number of doves and hawks at each generation
def VanillaGameLoop(creatures, num_food, iterations):
    totalDoves = []
    totalHawks = []

    # Game loop
    for i in range(0, iterations):
        foodLocations = InitializeFood(num_food)

        # Place creatures
        for creature in creatures:
            placed = PlaceCreature(creature, foodLocations, num_food)
            if not placed:
                creature.is_alive = False

        # Determine creatures status (dead or alive)
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

    return totalDoves, totalHawks


# Runs the game as explained in part two of the assignment description
# Returns the number of doves and hawks at each generation
def ModifiedGameLoop(creatures, num_food, iterations):
    totalDoves = []
    totalHawks = []

    # Game loop
    for i in range(0, iterations):
        foodLocations = ModifiedInitializeFood(num_food)

        # Place creatures
        for creature in creatures:
            ModifiedPlaceCreature(creature, foodLocations, num_food)

        # Determine creatures status (dead or alive)
        for location in foodLocations:
            residents = location.GetCreatures()
            ModifiedUpdateCreatures(residents)

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

    return totalDoves, totalHawks


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


# Updates the creatures based on their type using the modified rules
def ModifiedUpdateCreatures(residents):
    totalResidents = len(residents)
    hawks = FindHawks(residents)

    if totalResidents == 0:
        return
    
    if len(hawks) == 0:
        if totalResidents == 1:
            residents[0].is_alive = True
            residents[0].change_to_reproduce = 1.0
        else:
            probabilityOfSurvival = 2 / (totalResidents + 1) # TODO: does totalResidents need to have 1 added to it?
            for resident in residents:
                if random.random() < probabilityOfSurvival:
                    resident.is_alive = True
                    resident.change_to_reproduce = 0.0
                else:
                    resident.is_alive = False
                    resident.change_to_reproduce = 0.0
    else:
        if totalResidents == 1:
            residents[0].is_alive = True
            residents[0].change_to_reproduce = 1.0
        else:
            probabilityOfSurvival = 2 / ((totalResidents + 1)- len(hawks)) # TODO: does totalResidents need to have 1 added to it?
            for resident in residents:
                if resident.type == "Hawk":
                    # TODO: handle multiple hawks
                    resident.is_alive = True
                    resident.change_to_reproduce = 0.0
                else:
                    if random.random() < probabilityOfSurvival:
                        resident.is_alive = True
                        resident.change_to_reproduce = 0.0
                    else:
                        resident.is_alive = False
                        resident.change_to_reproduce = 0.0
        
    
# Returns a list of all the hawks in the list of residents
def FindHawks(residents):
    hawks = []
    for resident in residents:
        if resident.type == "Hawk":
            hawks.append(resident)
    return hawks


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


# Places a creature in a random food location
def ModifiedPlaceCreature(created_creature, foodLocations, num_food):
    location = random.randint(0, num_food - 1)
    foodLocations[location].AddCreature(created_creature)


# Populates the food array with the given number of food items
# Returns the food array using the vanilla food location
def InitializeFood(total_food):
    food = []
    for i in range(0, total_food):
        food.append(Objects.FoodLocation())

    return food


# Populates the food array with the given number of food items
# Returns the food array using the modified food location
def ModifiedInitializeFood(total_food):
    food = []
    for i in range(0, total_food):
        food.append(Objects.VariantFoodLocation())

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

    
# Main(["Game.py", "Dove", "Vanilla"])
# Main(["Game.py", "Hawk", "Vanilla"])
# Main(["Game.py", "Dove", "Modified"])
# Main(["Game.py", "Hawk", "Modified"])

# CollectData()

Main(sys.argv)