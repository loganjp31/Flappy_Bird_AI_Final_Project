import random

from neatAI.NodeGene import NodeGene
from neatAI.ConnectGene import ConnectGene


class Genome:
    def __init__(self):
        self.nodes = {}
        self.connections = {}
        self.fitness = 0.0
        self.adjusted_fitness = 0.0

    @staticmethod
    def create_base_genome(innovation_tracker):
        genome = Genome()

        genome.nodes[0] = NodeGene(0, NodeGene.INPUT, layer=0.0)
        genome.nodes[1] = NodeGene(1, NodeGene.INPUT, layer=0.0)
        genome.nodes[2] = NodeGene(2, NodeGene.INPUT, layer=0.0)
        genome.nodes[3] = NodeGene(3, NodeGene.INPUT, layer=0.0)
        genome.nodes[4] = NodeGene(4, NodeGene.BIAS, layer=0.0)

        genome.nodes[5] = NodeGene(5, NodeGene.OUTPUT, layer=1.0)

        for in_id in [0, 1, 2, 3, 4]:
            innov = innovation_tracker.get_connection_innovation(in_id, 5)
            genome.connections[innov] = ConnectGene(
                in_id, 5, random.uniform(-1, 1), True, innov
            )

        return genome

    def copy(self):
        new_genome = Genome()
        new_genome.nodes = {
            node_id: NodeGene(node.id, node.type, node.layer)
            for node_id, node in self.nodes.items()
        }
        new_genome.connections = {
            innov: conn.copy()
            for innov, conn in self.connections.items()
        }
        new_genome.fitness = 0.0
        new_genome.adjusted_fitness = 0.0
        return new_genome

    def forward(self, bird_y, bird_vel, pipe_dist, gap_y):
        for node in self.nodes.values():
            node.value = 0.0

        self.nodes[0].value = bird_y / 700.0
        self.nodes[1].value = bird_vel / 10.0
        self.nodes[2].value = pipe_dist / 400.0
        self.nodes[3].value = gap_y / 700.0
        self.nodes[4].value = 1.0

        ordered_nodes = sorted(self.nodes.values(), key=lambda n: (n.layer, n.id))

        for node in ordered_nodes:
            if node.type in (NodeGene.HIDDEN, NodeGene.OUTPUT):
                node.value = NodeGene.activate(node.value)

            for conn in self.connections.values():
                if conn.enabled and conn.in_node == node.id:
                    self.nodes[conn.out_node].value += node.value * conn.weight

        return self.nodes[5].value > 0.5

    def mutate_weights(self):
        for conn in self.connections.values():
            if random.random() < 0.85:
                conn.weight += random.uniform(-0.5, 0.5)
            else:
                conn.weight = random.uniform(-1, 1)

    def add_connection_mutation(self, innovation_tracker, max_tries=30):
        node_ids = list(self.nodes.keys())

        for _ in range(max_tries):
            a = random.choice(node_ids)
            b = random.choice(node_ids)

            if a == b:
                continue

            node_a = self.nodes[a]
            node_b = self.nodes[b]

            if node_a.layer >= node_b.layer:
                continue

            if node_b.type in (NodeGene.INPUT, NodeGene.BIAS):
                continue

            exists = any(
                c.in_node == a and c.out_node == b
                for c in self.connections.values()
            )
            if exists:
                continue

            innov = innovation_tracker.get_connection_innovation(a, b)
            self.connections[innov] = ConnectGene(
                a, b, random.uniform(-1, 1), True, innov
            )
            return

    def add_node_mutation(self, innovation_tracker):
        enabled_connections = [c for c in self.connections.values() if c.enabled]
        if not enabled_connections:
            return

        conn = random.choice(enabled_connections)
        conn.enabled = False

        in_layer = self.nodes[conn.in_node].layer
        out_layer = self.nodes[conn.out_node].layer
        new_layer = (in_layer + out_layer) / 2.0

        new_node_id = max(self.nodes.keys()) + 1
        self.nodes[new_node_id] = NodeGene(new_node_id, NodeGene.HIDDEN, layer=new_layer)

        innov1 = innovation_tracker.get_connection_innovation(conn.in_node, new_node_id)
        innov2 = innovation_tracker.get_connection_innovation(new_node_id, conn.out_node)

        self.connections[innov1] = ConnectGene(
            conn.in_node, new_node_id, 1.0, True, innov1
        )
        self.connections[innov2] = ConnectGene(
            new_node_id, conn.out_node, conn.weight, True, innov2
        )

    def mutate(self, innovation_tracker):
        self.mutate_weights()

        if random.random() < 0.10:
            self.add_connection_mutation(innovation_tracker)

        if random.random() < 0.06:
            self.add_node_mutation(innovation_tracker)