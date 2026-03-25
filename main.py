import asyncio
import os
import pygame

from game.Pipe import Pipe
from game.Base import Base
from ai.Agent import Agent
from ai.Genome import Genome
from ai.ga import evolve

pygame.init()
pygame.font.init()
pygame.display.set_caption("Flappy Bird GA")

WIN_WIDTH = 400
WIN_HEIGHT = 700
POPULATION_SIZE = 20
MAX_GENERATIONS = 50

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "images")

BG_IMG = pygame.transform.scale_by(
    pygame.image.load(os.path.join(IMG_DIR, "bg.png")), 1.5
)

STAT_FONT = pygame.font.SysFont("comicsans", 25)


def draw_window(win, agents, pipes, base, score, generation, best_fitness):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    score_text = STAT_FONT.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    gen_text = STAT_FONT.render(f"Gen: {generation}", True, (255, 255, 255))
    win.blit(gen_text, (10, 10))

    alive_count = sum(1 for agent in agents if agent.alive)
    alive_text = STAT_FONT.render(f"Alive: {alive_count}", True, (255, 255, 255))
    win.blit(alive_text, (10, 40))

    best_text = STAT_FONT.render(f"Best: {best_fitness:.2f}", True, (255, 255, 255))
    win.blit(best_text, (10, 70))

    base.draw(win)

    for agent in agents:
        if agent.alive:
            agent.bird.draw(win)

    pygame.display.flip()


def reset_game(genomes):
    agents = [Agent(genome=g) for g in genomes]
    base = Base(600)
    pipes = [Pipe(500)]
    score = 0
    return agents, base, pipes, score


async def run_generation(win, clock, genomes, generation, best_fitness_so_far):
    agents, base, pipes, score = reset_game(genomes)
    run = True

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        alive_agents = [agent for agent in agents if agent.alive]
        if not alive_agents:
            break #game resets when all agents are dead

        pipe_ind = 0
        if len(pipes) > 1 and alive_agents[0].bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        next_pipe = pipes[pipe_ind]

        for agent in agents:
            if agent.alive:
                agent.think(next_pipe)
                agent.bird.move()
                agent.genome.fitness += 0.1 #the agent is rewarded 0.1 for staying alive

        add_pipe = False
        removed_pipes = []

        for pipe in pipes:
            for agent in agents:
                if not agent.alive:
                    continue

                if pipe.collide(agent.bird):
                    agent.alive = False
                    agent.genome.fitness -= 2 #the agent is penalized 2 for colliding with a pipe

                if not pipe.passed and pipe.x < agent.bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(450))
            for agent in agents:
                if agent.alive:
                    agent.genome.fitness += 5 #the agent is rewarded 5 for passing a pipe

        for rp in removed_pipes:
            if rp in pipes:
                pipes.remove(rp)

        for agent in agents:
            if agent.alive:
                if agent.bird.y + agent.bird.img.get_height() >= 600 or agent.bird.y < 0:
                    agent.alive = False
                    agent.genome.fitness -= 2 #the agent is penalized 2 for hitting the ground or ceiling

        base.move()

        current_best = max(agent.genome.fitness for agent in agents)
        draw_window(win, agents, pipes, base, score, generation, max(best_fitness_so_far, current_best))

        await asyncio.sleep(0)

    return [agent.genome for agent in agents]


async def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    population = [Genome() for _ in range(POPULATION_SIZE)]
    best_fitness_so_far = float("-inf")

    for generation in range(1, MAX_GENERATIONS + 1):
        finished_genomes = await run_generation(
            win, clock, population, generation, best_fitness_so_far
        )

        generation_best = max(g.fitness for g in finished_genomes)
        best_fitness_so_far = max(best_fitness_so_far, generation_best)

        print(f"Generation {generation} best fitness: {generation_best:.2f}")

        population = evolve(finished_genomes, POPULATION_SIZE)

    pygame.quit()


asyncio.run(main())