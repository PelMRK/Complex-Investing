import random

import numpy as np
from numpy.random import randint
from random import random as rnd
from random import gauss


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


def individual(number_of_genes):
    ind = [randint(-100000, 100000) for x in range(number_of_genes)]
    return ind


def population(number_of_individuals, number_of_genes):
    return [individual(number_of_genes) for x in range(number_of_individuals)]


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


def mutate(population, num_ind, num_gen):
    for x in range(num_ind):
        delta = (num_ind - x + 1) / num_ind
        for g in range(num_gen):
            population["Individuals"][x][g] += gauss(0, 30*delta)*100
        population["Fitness"][x] = fitness_calculation(population["Individuals"][x])
    sorted_fitness = sorted([[population["Individuals"][x], population["Fitness"][x]] for x in range(num_ind)], key=lambda x: x[1])
    population = [sorted_fitness[x][0] for x in range(len(sorted_fitness))]
    fitness = [sorted_fitness[x][1] for x in range(len(sorted_fitness))]
    return {'Individuals': population, 'Fitness': sorted(fitness)}


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


num_ind = 10
num_gen = 153
pop = first_generation(population(num_ind, num_gen))
pop["Individuals"][-1] = read_pop('pop.txt')
while True:
    for x in range(10):
            pop = mutate(pop, num_ind, num_gen)
    record_pop(pop["Individuals"][-1], 'pop.txt')
    print(pop['Fitness'])



