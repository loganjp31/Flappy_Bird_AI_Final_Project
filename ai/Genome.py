import random

class Genome:
    def __init__(self, weights=None):
        self.weights = weights or [random.uniform(-1, 1) for _ in range(5)]
        self.fitness = 0

    def decide(self, bird_y, bird_vel, pipe_x, gap_y):
        w1, w2, w3, w4, bias = self.weights
        score = (
            w1 * bird_y + # height of the bird
            w2 * bird_vel + # vertical velocity of the bird
            w3 * pipe_x + # horizontal distance to the next pipe
            w4 * gap_y + # vertical distance to the gap
            bias # bias term, allows the bird to jump even if all other inputs are zero
        )
        return score > 0