from game.Bird import Bird
from ai.Genome import Genome


class Agent:
    def __init__(self, x=150, y=300, genome=None):
        self.bird = Bird(x, y)
        self.genome = genome if genome else Genome()
        self.alive = True

        self.frames_survived = 0
        self.pipes_passed = 0

    def think(self, next_pipe):
        bird_y = self.bird.y
        bird_vel = self.bird.vel
        pipe_dist = next_pipe.x - self.bird.x
        gap_y = next_pipe.height

        if self.genome.forward(bird_y, bird_vel, pipe_dist, gap_y):
            self.bird.jump()