import numpy as np
from numpy.random import randint
from random import random as rnd
from random import gauss  # , randrange


def individual(number_of_genes, upper_limit, lower_limit):
    individual = [rnd() * (upper_limit - lower_limit) + lower_limit for x in range(number_of_genes)]
    return individual


def population(number_of_individuals, number_of_genes, upper_limit, lower_limit):
    return [individual(number_of_genes, upper_limit, lower_limit) for x in range(number_of_individuals)]


def values(weights, info):
    vals = []
    for x in range(len(info)):
        val = 0
        for y in range(len(info[x])):
            val += info[x][y] * weights[y]
        if val < 0:
            val = 0
        vals.append(val)
    return vals


def fitness_calculation(individual):
    global info
    vls = values(individual, info)
    prc = []
    for el in vls:
        prc.append(el / sum(vls))
    summa = 0
    for i in range(len(prc)):
        summa += prc[i] * pr_delta[i]
    if max(prc) > 0.5:
        summa = -1
    return summa


def selection(generation, method='Fittest Half'):
    generation['Normalized Fitness'] = sorted([generation['Fitness'][x] / sum(generation['Fitness'])
                                               for x in range(len(generation['Fitness']))], reverse=True)
    generation['Cumulative Sum'] = np.array(generation['Normalized Fitness']).cumsum()
    if method == 'Fittest Half':
        selected_individuals = [generation['Individuals'][-x - 1]
                                for x in range(int(len(generation['Individuals']) // 2))]
        selected_fitnesses = [generation['Fitness'][-x - 1]
                              for x in range(int(len(generation['Individuals']) // 2))]
        selected = {'Individuals': selected_individuals, 'Fitness': selected_fitnesses}
    elif method == 'Random':
        selected_individuals = [generation['Individuals'][randint(1, len(generation['Fitness']))]
                                for x in range(int(len(generation['Individuals']) // 2))]
        selected_fitnesses = [generation['Fitness'][-x - 1]
                              for x in range(int(len(generation['Individuals']) // 2))]
        selected = {'Individuals': selected_individuals, 'Fitness': selected_fitnesses}
    return selected


def pairing(elit, selected, method='Random'):
    individuals = [elit['Individuals']]+selected['Individuals']
    fitness = [elit['Fitness']]+selected['Fitness']
    if method == 'Fittest':
        parents = [[individuals[x], individuals[x+1]] for x in range(len(individuals)//2)]
    elif method == 'Random':
        parents = []
        for x in range(len(individuals)//2):
            parents.append([individuals[randint(0, (len(individuals)-1))],
                            individuals[randint(0, (len(individuals)-1))]])
            while parents[x][0] == parents[x][1]:
                parents[x][1] = individuals[randint(0, (len(individuals)-1))]
    return parents


def mating(parents, method='Single Point'):
    if method == 'Single Point':
        pivot_point = randint(1, len(parents[0]))
        offsprings = [parents[0][0:pivot_point] + parents[1][pivot_point:],
                      parents[1][0:pivot_point] + parents[0][pivot_point:]]
    elif method == 'Two Points':
        pivot_point_1 = randint(1, len(parents[0])-1)
        pivot_point_2 = randint(1, len(parents[0]))
        while pivot_point_2 < pivot_point_1:
            pivot_point_2 = randint(1, len(parents[0]))
        offsprings = [
            parents[0][0:pivot_point_1] + parents[1][pivot_point_1:pivot_point_2] + parents[0][pivot_point_2:],
            parents[1][0:pivot_point_1] + parents[0][pivot_point_1:pivot_point_2] + parents[1][pivot_point_2:]]
        offsprings = offsprings
    return offsprings


def mutate(population, upper_limit, lower_limit, num_ind, num_gen):
    for x in range(num_ind):
        delta = (num_ind - x + 1) / num_ind
        for g in range(num_gen):
            population[x][g] += gauss(0, 3*delta)*100
            print("dsffs")
    return population


def next_generation(gen, upper_limit, lower_limit, num_ind, num_gen):
    elit = {}
    next_gen = {}
    # elit['Individuals'] = gen['Individuals'].pop(-1)
    # elit['Fitness'] = gen['Fitness'].pop(-1)
    selected = selection(gen)
    parents = pairing(elit, selected)
    offsprings = [[[mating(parents[x]) for x in range(len(parents))]
                  [y][z] for z in range(2)] for y in range(len(parents))]
    offsprings1 = [offsprings[x][0] for x in range(len(parents))]
    offsprings2 = [offsprings[x][1] for x in range(len(parents))]
    unmutated = selected['Individuals']+offsprings1+offsprings2
    mutated = mutate(unmutated, upper_limit, lower_limit, num_ind, num_gen)
    unsorted_individuals = mutated + [elit['Individuals']]
    unsorted_next_gen = [fitness_calculation(mutated[x]) for x in range(len(mutated))]
    unsorted_fitness = [unsorted_next_gen[x] for x in range(len(gen['Fitness']))] + [elit['Fitness']]
    sorted_next_gen = sorted([[unsorted_individuals[x], unsorted_fitness[x]]
                              for x in range(len(unsorted_individuals))], key=lambda x: x[1])
    next_gen['Individuals'] = [sorted_next_gen[x][0] for x in range(len(sorted_next_gen))]
    next_gen['Fitness'] = [sorted_next_gen[x][1] for x in range(len(sorted_next_gen))]
    gen['Individuals'].append(elit['Individuals'])
    gen['Fitness'].append(elit['Fitness'])
    return next_gen


# Generations and fitness values will be written to this file
Result_file = 'GA_Results.txt'  # Creating the First Generation


def first_generation(pop):
    fitness = [fitness_calculation(pop[x]) for x in range(len(pop))]
    sorted_fitness = sorted([[pop[x], fitness[x]] for x in range(len(pop))], key=lambda x: x[1])
    population = [sorted_fitness[x][0] for x in range(len(sorted_fitness))]
    fitness = [sorted_fitness[x][1] for x in range(len(sorted_fitness))]
    return {'Individuals': population, 'Fitness': sorted(fitness)}


def read_info(filename, delimiter='\n'):
    with open(filename, 'r') as f:
        lines = f.read().split(delimiter)
    info = []
    for el in lines:
        info.append(el.split('\t'))
    for i in range(len(info)):
        for j in range(len(info[i])):
            try:
                info[i][j] = float(info[i][j].replace(",", "."))
            except:
                info[i][j] = 0
    return info


def read_weights(filename, delimiter='\t'):
    with open(filename, 'r') as f:
        lines = f.read().split(delimiter)
    for x in range(len(lines)):
        lines[x] = float(lines[x].replace(",", "."))
    return lines


def read_prices(filename, delimiter='\n'):
    with open(filename, 'r') as f:
        lines = f.read().split(delimiter)
    for x in range(len(lines)):
        lines[x] = float(lines[x].replace(",", "."))
    return lines


def record_pop(data_list, filename, delimiter='\t'):
    my_file = open(filename, 'w')
    for elem in data_list:
        my_file.write(str(elem) + delimiter)


def read_pop(filename='pop.txt', delimiter='\t'):
    with open(filename, 'r') as f:
        lines = f.read().split(delimiter)
    lines = lines[:-1]
    for i in range(len(lines)):
        lines[i] = float(lines[i])
    return lines


info = read_info('info.txt')
weights = read_weights('weights.txt')
pr_delta = read_prices('price_delta.txt')

num_ind = 100
num_gen = 153
max_genv = 10000
min_genv = -10000
pop = population(num_ind, num_gen, max_genv, min_genv)
gen = first_generation(pop)
# gen["Individuals"][-1] = read_pop('pop.txt')
while True:
    for i in range(1000):
        try:
            gen = next_generation(gen, max_genv, min_genv, num_ind, num_gen)
        except:
            None
    record_pop(gen["Individuals"][-1], 'pop.txt')
    # print(gen["Fitness"])
