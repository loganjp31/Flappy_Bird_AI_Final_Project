import random


class Species:
    def __init__(self, representative):
        self.representative = representative.copy()
        self.members = []
        self.best_fitness = float("-inf")

    def add_member(self, genome):
        self.members.append(genome)

    def clear(self):
        self.members = []

    def sort_members(self):
        self.members.sort(key=lambda g: g.fitness, reverse=True)

        if self.members and self.members[0].fitness > self.best_fitness:
            self.best_fitness = self.members[0].fitness
            self.representative = self.members[0].copy()

    def compute_adjusted_fitness(self):
        size = len(self.members)
        if size == 0:
            return

        for genome in self.members:
            genome.adjusted_fitness = genome.fitness / size

    def select_parent(self):
        if not self.members:
            return None

        total = sum(max(g.adjusted_fitness, 0.0) + 1e-6 for g in self.members)

        if total <= 0:
            return random.choice(self.members)

        pick = random.uniform(0, total)
        current = 0.0

        for genome in self.members:
            current += max(genome.adjusted_fitness, 0.0) + 1e-6
            if current >= pick:
                return genome

        return self.members[0]