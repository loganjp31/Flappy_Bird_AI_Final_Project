import random
from ai.Genome import Genome


def select_parent(genomes):
    total_fitness = sum(max(g.fitness, 0) + 1 for g in genomes) 
    pick = random.uniform(0, total_fitness)
    current = 0

    for genome in genomes:
        current += max(genome.fitness, 0) + 1
        if current >= pick:
            return genome

    return genomes[0] 


def crossover(parent1, parent2):
    child_weights = [
        random.choice([w1, w2]) for w1, w2 in zip(parent1.weights, parent2.weights)
    ]
    return Genome(weights=child_weights)


def mutate(genome, mutation_rate=0.1, mutation_strength=0.5):
    new_weights = genome.weights[:]

    for i in range(len(new_weights)):
        if random.random() < mutation_rate:
            new_weights[i] += random.uniform(-mutation_strength, mutation_strength)

    return Genome(weights=new_weights)


def evolve(old_genomes, population_size):
    old_genomes.sort(key=lambda g: g.fitness, reverse=True)

    elite_count = max(2, population_size // 5)
    elites = old_genomes[:elite_count]

    new_population = [Genome(weights=g.weights[:]) for g in elites]

    while len(new_population) < population_size:
        parent1 = select_parent(elites)
        parent2 = select_parent(elites)

        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate=0.2, mutation_strength=0.4)

        new_population.append(child)

    return new_population