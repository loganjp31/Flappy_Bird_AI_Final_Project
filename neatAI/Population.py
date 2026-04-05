import random

from neatAI.Genome import Genome
from neatAI.Species import Species
from neatAI.ga_utils import crossover, compatibility_distance
from neatAI.InnovationTracker import InnovationTracker


class Population:
    def __init__(self, size, elite_count=1):
        self.size = size
        self.elite_count = elite_count
        self.innovation_tracker = InnovationTracker()
        self.genomes = [
            Genome.create_base_genome(self.innovation_tracker)
            for _ in range(size)
        ]
        self.species = []
        self.generation = 0
        self.best_genome = None

    def speciate(self, threshold=3.0):
        for species in self.species:
            species.clear()

        for genome in self.genomes:
            placed = False

            for species in self.species:
                if compatibility_distance(genome, species.representative) < threshold:
                    species.add_member(genome)
                    placed = True
                    break

            if not placed:
                new_species = Species(genome)
                new_species.add_member(genome)
                self.species.append(new_species)

        self.species = [s for s in self.species if s.members]

    def update_best_genome(self):
        if not self.genomes:
            return

        current_best = max(self.genomes, key=lambda g: g.fitness)

        if self.best_genome is None or current_best.fitness > self.best_genome.fitness:
            self.best_genome = current_best.copy()

    def evolve(self):
        self.generation += 1
        self.speciate()

        for species in self.species:
            species.sort_members()
            species.compute_adjusted_fitness()

        self.update_best_genome()

        new_genomes = []

        # -------- ELITISM --------
        # 1. Keep best genome from every species
        for species in self.species:
            if species.members:
                new_genomes.append(species.members[0].copy())

        # 2. Keep top N genomes overall
        sorted_all = sorted(self.genomes, key=lambda g: g.fitness, reverse=True)
        for elite in sorted_all[:self.elite_count]:
            new_genomes.append(elite.copy())

        # 3. Keep global best genome again if somehow missing
        if self.best_genome is not None:
            new_genomes.append(self.best_genome.copy())

        # Remove duplicates by structure + fitness snapshot
        unique = []
        seen = set()
        for genome in new_genomes:
            key = (
                tuple(sorted(genome.nodes.keys())),
                tuple(
                    (c.in_node, c.out_node, round(c.weight, 6), c.enabled, c.innovation)
                    for c in sorted(genome.connections.values(), key=lambda x: x.innovation)
                ),
            )
            if key not in seen:
                seen.add(key)
                unique.append(genome)

        new_genomes = unique[:self.size]

        species_scores = [
            sum(max(g.adjusted_fitness, 0.0) for g in species.members)
            for species in self.species
        ]

        total_species_score = sum(species_scores)

        while len(new_genomes) < self.size:
            if not self.species:
                child = Genome.create_base_genome(self.innovation_tracker)
                child.mutate(self.innovation_tracker)
                new_genomes.append(child)
                continue

            if total_species_score <= 0:
                species = random.choice(self.species)
            else:
                pick = random.uniform(0, total_species_score)
                current = 0.0
                species = self.species[0]

                for s, score in zip(self.species, species_scores):
                    current += score
                    if current >= pick:
                        species = s
                        break

            parent1 = species.select_parent()
            parent2 = species.select_parent()

            if parent1 is None:
                child = Genome.create_base_genome(self.innovation_tracker)
            elif parent2 is None:
                child = parent1.copy()
            else:
                if parent1 is parent2:
                    child = parent1.copy()
                else:
                    child = crossover(parent1, parent2)

            child.mutate(self.innovation_tracker)
            new_genomes.append(child)

        self.genomes = new_genomes[:self.size]