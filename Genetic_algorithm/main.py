# Authors:
#  B85066 Paula Monge
#  B87095 Josef Ruzicka

import random
import timeit
import numpy as np
import statistics
import time
import matplotlib.pyplot as plt 

WORKERS_NUMBER = 4
MAX_CAPACITY = 2000
PENDING_TASKS = []
POPULATION_SIZE = 30
GENERATIONS = 2000
NUMBER_OF_TASKS = 50

# A workers list
WORKERS = [[] for _ in range(WORKERS_NUMBER)]
GENETIC_WORKERS = [[[] for _ in range(WORKERS_NUMBER)] for _ in range(POPULATION_SIZE)]

# Function that generates the taks to be executed by the workers
def create_random_task():
  # Create a very big list of random numbers between 0 and 100
  return [random.randint(1, 6) for i in range(NUMBER_OF_TASKS)]

# ----------- Brute Force ------------
# Create a function that returns every possible combination of a list of items with a given capacity
def brute_force_aux(items, capacity):
    # Create a list to store the possible combinations
    possible_combinations = []

    # Create a list to store the current combination
    current_combination = []

    # Create a function to recursively find all possible combinations
    def find_combinations(items, capacity, current_combination, possible_combinations):
        # If the capacity is 0, then we have found a possible combination
        if capacity == 0:
            possible_combinations.append(current_combination)
            return

        # If the capacity is negative, then we have overshot and we should return
        if capacity < 0:
            return

        # If there are no items left, then we have reached the end of the list and should return
        if not items:
            return

        # Create a new list of items that excludes the first item in the list
        new_items = items[1:]

        # Create a new list that includes the first item in the list
        new_combination = current_combination + [items[0]]

        # Recursively call the function with the new items and new combination
        find_combinations(new_items, capacity, current_combination, possible_combinations)
        find_combinations(new_items, capacity - items[0], new_combination, possible_combinations)

    # Call the recursive function
    find_combinations(items, capacity, current_combination, possible_combinations)

    # Return the possible combinations
    return possible_combinations

# create a queue system with a given number of workers and a given capacity for each worker and the list pending_list of tasks to be done by the workers and distribute the tasks among the workers using the brute force algorithm
def queue_system_brute_force(number_workers, capacity, pending_list):
    # create a list of workers
    workers = []

    # create a list of tasks for each worker
    for worker in range(number_workers):
        workers.append([])

    # find all possible combinations of tasks for each worker
    possible_combinations = brute_force_aux(pending_list, capacity)

    # find the combination with the least amount of tasks
    best_combination = possible_combinations[0]
    for combination in possible_combinations:
        if len(combination) < len(best_combination):
            best_combination = combination

    # distribute the tasks among the workers
    for task in best_combination:
        worker = random.randint(0, number_workers-1)
        workers[worker].append(task)

    # return the workers
    return workers

my_pending_list = [random.randint(1, 6) for i in range(25)]

def brute_force():
  workers = queue_system_brute_force(10, 50, my_pending_list)
  for worker in workers:
    print("CPU load: ", sum(worker), worker)

# ----------- Heurisitc ------------
# For each task, check every worker and assign it to the least loaded one.
def heuristic():
  for task in PENDING_TASKS:
    lowestWorkerLoad = MAX_CAPACITY
    # Select least loaded worker.
    for worker in WORKERS:
      if sum(worker) < lowestWorkerLoad:
        lowestWorker = worker
        lowestWorkerLoad = sum(worker)
    lowestWorker.append(task)
  
  # Print results for demo.
  for worker in WORKERS:
    print("Carga de CPU: ", sum(worker), worker)
  #print("Distribución de trabajo: ", WORKERS)
  pass

# ---------- Metaheuristic ------------
# Using a genetic algorithm
def genetic_algorithm():
  # 1. Generate random population
  population = generate_population()
  for gen in range(GENERATIONS):
    # 2. get fitness
    individualsScores = fitness(population)
    # 3. select top 20% & bot 10% 
    possibleParents = selection(individualsScores)
    # 4. Crossover
    newPopulation = crossover(possibleParents, individualsScores)
    # 5. mutate
    population = mutation(newPopulation)

    if gen % 250 == 0:
      print("GEN:", gen)
      for individual in range(len(population)):
        if (individual % 50 == 0):
          print("Individual: ", individual, population[individual])
      print("best fit: ", min(individualsScores))
      print('')

  # get best individual.
  bestIndividual = population[individualsScores.index(min(individualsScores))]
  print("Best individual: ", bestIndividual)

# Generates a random distribuition of tasks for each individual.
def generate_population():
  for individual in range(POPULATION_SIZE):
    for task in PENDING_TASKS:
      worker = random.randint(0, WORKERS_NUMBER-1)
      GENETIC_WORKERS[individual][worker].append(task)

  return GENETIC_WORKERS

# fitness function: mean individuals worker load.
# the lower the fitness score, the better. 
def fitness(population):
  suma = 0
  score = []

  for individual in range(POPULATION_SIZE):
    sumas = []
    for worker in range(WORKERS_NUMBER):
      suma = sum(population[individual][worker])
      sumas.append(suma)

    _mean = np.std(sumas)
    score.append(_mean)

  return score

def selection(individualScores):
  newScore = np.sort(individualScores)
  bestIndividuals = newScore[0 : int(POPULATION_SIZE * 0.2)]
  wortIndividuals = newScore[int(POPULATION_SIZE * 0.9) : -1]

  selectedIndividuals = np.concatenate((bestIndividuals, wortIndividuals), axis=None)

  return selectedIndividuals

def crossover(parents, individualsScores):
  # Select random parents
  randP1 = random.randint(0, len(parents)-1)
  randP2 = random.randint(0, len(parents)-1)

  indexP1 = individualsScores.index(parents[randP1])
  indexP2 = individualsScores.index(parents[randP2])

  # Crossover
  newPopulation = []

  for individual in range(POPULATION_SIZE):
    newIndividual = []
    pending_tasks = PENDING_TASKS.copy()
  
    for worker in range(WORKERS_NUMBER):
      # Choose a parent.
      if random.random() < 0.5:
        parentIndex = indexP1
      else: 
        parentIndex = indexP2

      # Generate a new worker, copying one from the father and removing the tasks that the new individual already inherited in another worker.
      newWorker = GENETIC_WORKERS[parentIndex][worker].copy()
      for i in GENETIC_WORKERS[parentIndex][worker]:
        # Mark tasks as distributed or remove them if they already had been marked.
       
        if i in pending_tasks:
          pending_tasks.remove(i)
        else:
          newWorker.remove(i)

      newIndividual.append(newWorker)

    # append remaining tasks to last worker which is more likely to be the emptiest one.
    for i in pending_tasks:
      newIndividual[-1].append(i)

    newPopulation.append(newIndividual)

  return newPopulation

def mutation(newPopulation):
  for individual in newPopulation:
    if random.random() < 0.1:
      randW1 = random.randint(0, WORKERS_NUMBER-1)
      randW2 = random.randint(0, WORKERS_NUMBER-1)

      # Intercambiar tareas
      randT1 = random.randint(0, len(individual[randW1])-1)
      randT2 = random.randint(0, len(individual[randW2])-1)
      tempTask = individual[randW1][randT1]

      individual[randW1][randT1] = individual[randW2][randT2]
      individual[randW2][randT2] = tempTask

      tempWorker = individual[randW1].copy()

      # Intercambiar trabajadores
      individual[randW1] = individual[randW2]
      individual[randW2] = tempWorker

  return newPopulation

# ----------- Results ---------------
PENDING_TASKS = create_random_task()
# print("# ----------- Brute Force ------------")
# brute_force()
# print("# ----------- Heuristic ------------")
# heuristic()
# print("# ----------- Metaheuristic ------------")
# genetic_algorithm()

# Record time execution for each algorithm.
brute_force_time = timeit.timeit("brute_force()", setup="from __main__ import brute_force", number=1)
heuristic_time = timeit.timeit("heuristic()", setup="from __main__ import heuristic", number=1)
genetic_algorithm_time = timeit.timeit("genetic_algorithm()", setup="from __main__ import genetic_algorithm", number=1)

print("Brute Force: ", brute_force_time)
print("Heuristic: ", heuristic_time)
print("Genetic Algorithm: ", genetic_algorithm_time)


