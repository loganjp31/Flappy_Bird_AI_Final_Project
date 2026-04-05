class ConnectGene:
    def __init__(self, in_node, out_node, weight, enabled, innovation):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation

    def copy(self):
        return ConnectGene(
            self.in_node,
            self.out_node,
            self.weight,
            self.enabled,
            self.innovation,
        )