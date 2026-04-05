import random

from neatAI.Genome import Genome
from neatAI.NodeGene import NodeGene


def crossover(parent1, parent2):
    # parent1 should be fitter
    if parent2.fitness > parent1.fitness:
        parent1, parent2 = parent2, parent1

    child = Genome()

    all_nodes = {}
    for node_id, node in parent1.nodes.items():
        all_nodes[node_id] = NodeGene(node.id, node.type)

    for node_id, node in parent2.nodes.items():
        if node_id not in all_nodes:
            all_nodes[node_id] = NodeGene(node.id, node.type)

    child.nodes = all_nodes

    for innov, gene1 in parent1.connections.items():
        gene2 = parent2.connections.get(innov)

        if gene2 is not None:
            chosen = random.choice([gene1, gene2]).copy()

            # Disabled genes often stay disabled
            if (not gene1.enabled or not gene2.enabled) and random.random() < 0.75:
                chosen.enabled = False
        else:
            chosen = gene1.copy()

        child.connections[innov] = chosen

    return child


def compatibility_distance(g1, g2, c1=1.0, c2=1.0, c3=0.4):
    innovations1 = set(g1.connections.keys())
    innovations2 = set(g2.connections.keys())

    if not innovations1 and not innovations2:
        return 0.0

    matching = innovations1 & innovations2
    non_matching = innovations1 ^ innovations2

    max1 = max(innovations1) if innovations1 else 0
    max2 = max(innovations2) if innovations2 else 0
    min_max = min(max1, max2)

    excess = 0
    disjoint = 0

    for innov in non_matching:
        if innov > min_max:
            excess += 1
        else:
            disjoint += 1

    avg_weight_diff = 0.0
    if matching:
        avg_weight_diff = sum(
            abs(g1.connections[i].weight - g2.connections[i].weight)
            for i in matching
        ) / len(matching)

    n = max(len(innovations1), len(innovations2))
    if n < 20:
        n = 1

    return (c1 * excess / n) + (c2 * disjoint / n) + (c3 * avg_weight_diff)