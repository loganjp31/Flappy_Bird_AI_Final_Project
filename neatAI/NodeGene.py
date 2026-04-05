import math


class NodeGene:
    INPUT = "input"
    HIDDEN = "hidden"
    OUTPUT = "output"
    BIAS = "bias"

    def __init__(self, node_id, node_type, layer=0.0):
        self.id = node_id
        self.type = node_type
        self.layer = layer
        self.value = 0.0

    @staticmethod
    def activate(x):
        x = max(-60, min(60, x))
        return 1.0 / (1.0 + math.exp(-x))