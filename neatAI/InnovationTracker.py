class InnovationTracker:
    def __init__(self):
        self.current_innovation = 0
        self.connection_history = {}

    def get_connection_innovation(self, in_node, out_node):
        key = (in_node, out_node)

        if key not in self.connection_history:
            self.current_innovation += 1
            self.connection_history[key] = self.current_innovation

        return self.connection_history[key]