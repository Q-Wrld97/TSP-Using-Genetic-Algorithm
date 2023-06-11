import random
import math
import matplotlib.pyplot as plt

#generate cities
def generate_cities (n=25, width=200, height=200):
  cities= {}
  random.seed(1) #setting the seed to 1 for reproducibility
  for i in range (n): #generating n cities
    x = random.uniform(0, width)  #random x coordinate 0-200
    y = random.uniform(0, height) #random y coordinate 0-200
    cities[i+1] = (int(x),int(y)) #adding the city to the dictionary
  return cities 

#calculate distance between two cities
def calculate_distance (cityA, cityB): 
  xDis = abs(cityA[0] - cityB[0])
  yDis = abs(cityA[1] - cityB[1])
  return (math.sqrt((xDis**2)+(yDis**2))) #distance between two points formula

#creating the inital population for the genetic algorithm
def create_Initial_Population (size_population,size_cities):
  population = []
  random.seed() 
  for i in range (size_population): #creating a population of n solutions
      population.append(random.sample(range(1, size_cities+1), size_cities))   #creating a solution of n cities but with no duplicates
  return population

#calculating the fitness of each solution
def fitness (population,cityList):
  fitness_per_solution= [] #list of fitness for per solution
  fitness = [] #list of fitness for each solution
  for i in range (len(population)): #for each solution
    for j in range (len(population[i])):  #for each city in the solution    
      try:
        fitness_per_solution.append(int(calculate_distance(cityList[population[i][j]],cityList[population[i][j+1]]))) #calculating the distance between two cities
      except IndexError:
        fitness_per_solution.append(int(calculate_distance(cityList[population[i][j]],cityList[population[i][0]]))) #calculating the distance between the last city and the first city
    fitness.append(sum(fitness_per_solution)) #summing the distance between all cities in the solution
    fitness_per_solution= [] #list of fitness for per solution
  return fitness  

#Selecting two parents from the that 50% of the population that have the lowest fitness (distance)
def selection(population,fitness):
  population_fitness = {}
  for i in range (len(population)): #creating a dictionary of the population and their fitness   
    population_fitness[i] = fitness[i]
  fittest_50_percent = [] 
  for i in range (len(population)):
    if population_fitness[i] <= (sum(population_fitness.values())/len(population)): #selecting top 50% of the population
      fittest_50_percent.append(i)
    else:
      pass
  random.seed()#Reset the seeds so we dont get the same value
  parent1= random.choice(fittest_50_percent) #selecting a random parent from the 50% of the population that have the lowest fitness (distance)
  parent2= random.choice(fittest_50_percent) #selecting a random parent from the 50% of the population that have the lowest fitness (distance)
  #validating that the two parents are not the same
  while parent1 == parent2:
    parent2= random.choice(fittest_50_percent) #selecting a random parent from the 50% of the population that have the lowest fitness (distance)
    
  return parent1,parent2

#Order cross over breeding
def order_crossover_breed (Parent1,Parent2):
  childP1 = [] #child solution from parent 1
  childP2 = [] #child solution from parent 2
  random.seed() #Reset the seeds so we dont get the same value
  geneA = int(random.random() * len(Parent1)) #creating a random index from parent 1
  geneB = int(random.random() * len(Parent1)) #creating a random index from parent 1
  startGene = min(geneA, geneB) #selecting the least index as the starting point
  endGene = max(geneA, geneB) #selecting the highest index as the ending point
  for i in range(startGene, endGene): #for each gene in the selected range
    childP1.append(Parent1[i]) #adding the gene to the child solution from parent 1
  childP2 = [item for item in Parent2 if item not in childP1] #adding the gene to the child solution from parent 2 that are not already in the child solution from parent 1
  child = childP1 + childP2 #adding the two child solutions together
  return child

def mutation(population, mutation_rate = 0.05):
  geneA = int(random.random() * len(population)) #creating a random index from parent 1
  geneB = int(random.random() * len(population)) #creating a random index from parent 2
  startGene = min(geneA, geneB) #selecting the least index as the starting point
  endGene = max(geneA, geneB) #selecting the highest index as the ending point 
  random.seed()
  if (random.random() < mutation_rate): # Only mutate if the random number is less than mutation rate
    for i in range(startGene, endGene): #for each gene in the selected range
            randomSpot = random.randint(0, len(population[i])-1)
            randomSpot2 = random.randint(0, len(population[i])-1)
            population[i][randomSpot],population[i][randomSpot2] = population[i][randomSpot2],population[i][randomSpot] #swapping the genes
  return population

#create a new population of n-2 solutions by breeding the fittest 50% of the population
def generate_new_population (population,fitness,eliteSize):
  new_population = []
  for i in range (len(population)-eliteSize): #creating a new population of n-2 solutions
    parent1,parent2 = selection(population,fitness)
    new_population.append(order_crossover_breed(population[parent1],population[parent2]))
  #picking the two fittest parents and adding them to the new population (elitism)
  population_fitness = {}
  for i in range (len(population)): #creating a dictionary of the population and their fitness
    population_fitness[i] = fitness[i]
  population_fitness = sorted(population_fitness.items(), key=lambda x: x[1]) #sorting the population by fitness (distance)
  for i in range (eliteSize):
    new_population.append(population[population_fitness[i][0]]) #adding the fittest parent to the new population
 
  return new_population

def best_fitness(population,fitness):
  population_fitness = {}
  for i in range (len(population)): #creating a dictionary of the population and their fitness
    population_fitness[i] = fitness[i]
  population_fitness = sorted(population_fitness.items(), key=lambda x: x[1]) #sorting the population by fitness (distance)
  return population[population_fitness[0][0]],population_fitness[0][1] #returning the fittest solution and its fitness (distance)

def evolution(population,fitnessArray,mutation_rate,cityList,eliteSize):
  new_population = generate_new_population(population,fitnessArray,eliteSize)
  mutated_population = mutation(new_population,mutation_rate)
  fitnessArray = fitness(mutated_population,cityList)
  bestSolution, bestDistance = best_fitness(mutated_population, fitnessArray)
  return mutated_population, fitnessArray, bestSolution, bestDistance

if __name__ == "__main__":
  cities = 25
  population = 100
  generation  = 0
  max_generations = math.inf
  mutation_rate = 0.05
  eliteSize= 5
  cityList = generate_cities(cities)
  
  
  print(f"Cities: {cities} Population: {population} Generations: {max_generations} Mutation Rate: {mutation_rate*100}% Elite Size= {eliteSize} \n\n\n")
  population = create_Initial_Population(population,cities)
  fitnessArray = fitness(population,cityList)
  bestSolution, bestDistance = best_fitness(population, fitnessArray)
  print(f"Generation 0: Best Solution: {bestSolution} Best Distance: {bestDistance}")

  last_two_hundred_distances = []
  while generation < max_generations:
      population, fitnessArray, bestSolution, bestDistance = evolution(population, fitnessArray, mutation_rate,cityList,eliteSize)
      print(f"Generation {generation+1}: Best Solution: {bestSolution} Best Distance: {bestDistance}")
      
      # Add the new bestDistance to the list
      last_two_hundred_distances.append(bestDistance)

      # If there are more than 300 distances in the list, remove the oldest one
      if len(last_two_hundred_distances) > 300:
          last_two_hundred_distances.pop(0)
      
      # Check if all distances in the list are the same, but only after 300 generations
      if generation >= 300 and len(set(last_two_hundred_distances)) == 1:
          print("The best distance didn't change for the last 300 generations")
          break

      generation += 1