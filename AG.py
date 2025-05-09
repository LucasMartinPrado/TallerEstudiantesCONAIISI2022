import array
import random
import math

from deap import base
from deap import creator
from deap import tools

def evaluate_population(population, level):
    list = []
    # Evaluamos a cada individuo
    for indiv in population:
        ###------Funcion de aptitud------###
        fit = math.dist([indiv.x, indiv.y], level.finish_position())
        ###------Fin de la funcion------###
        list.append((fit,))
    return list

'''
def evaluate_population(population, level):
    list = []
    # Evaluamos a cada individuo
    for indiv in population:
        ###------Funcion de aptitud------###
        if indiv.finished:
            fit = indiv.currentMove - len(indiv.moves)
        elif indiv.alive:
            fit = math.dist([indiv.x, indiv.y], level.finish_position())
        else: #not finished, and not alive
            fit = 1000000

        ###------Fin de la funcion------###
        list.append((fit,))
    return list

def evaluate_population(population, level): #Analizando varias posiciones
    list = []
    # Evaluamos a cada individuo
    for indiv in population:
       ###------Funcion de aptitud------###
       if indiv.finished:
           fit = indiv.currentMove - len(indiv.moves)
       elif indiv.alive:
           # Usando más de una posición para calcular aptitud
           fit = sum([math.dist(level.finish_position(),
    [indiv.historic_x[k], indiv.historic_y[k]]) - 10.00 for k, _ in enumerate(indiv.moves) if (k+1) % 50 == 0])
       else:
           fit = 15000.00 * (1 + len(indiv.moves) - indiv.currentMove)
       ###------Fin de la funcion------###
       list.append((fit,))
    return list

'''

class AG:
    def __init__(self, level, population, ind_size):
        #Initializing the creator - Defining Fitness function and individual
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)
        #Attributes
        self.level = level
        self.toolbox = base.Toolbox()
        self.load_toolbox(ind_size)
        self.population = self.toolbox.population(n=population)
        self.generation = 0


    def update_toolbox(self, ag, size, best_ind):
        self.level = ag.level
        self.toolbox = base.Toolbox()
        self.load_toolbox(size)
        self.population = self.toolbox.population(len(self.population))
        for individual in self.population:
            for i in range(len(best_ind)):
                individual[i] = best_ind[i]
        self.generation = ag.generation

    def load_toolbox(self, ind_size):
        self.toolbox.register("movements", random.randint, 0, 7)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.movements, ind_size)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", tools.cxUniform, indpb=0.7)
        self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=7, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", evaluate_population)

    def evolution_step(self):
        # CXPB  is the probability with which two individuals are crossed
        # MUTPB is the probability for mutating an individual
        CXPB, MUTPB = 0.5, 0.25
        pop = self.population
        self.generation += 1
        # Select the next generation of individuals
        offspring = self.toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(self.toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                self.toolbox.mate(child1, child2)

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                self.toolbox.mutate(mutant)
        # Add back the best 1 (Elitism)
        offspring.extend(tools.selBest(self.population, 1))
        # Save the population
        self.population = offspring

    def fitness_evaluation(self, population):
        # Evaluate the individuals
        fitnesses = self.toolbox.evaluate(population, self.level)
        for ind, fit in zip(self.population, fitnesses):
            ind.fitness.values = fit
        best_ind = tools.selBest(self.population, 1)[0]
        return best_ind


