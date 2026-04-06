import asyncio
import os
import pygame

from game.Pipe import Pipe
from game.Base import Base
from neatAI.Agent import Agent
from neatAI.Population import Population

pygame.init()
pygame.font.init()
pygame.display.set_caption("Flappy Bird NEAT")

WIN_WIDTH = 400
WIN_HEIGHT = 700
POPULATION_SIZE = 100
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


def draw_pause_text(win):
    pause_font = pygame.font.SysFont("comicsans", 50)
    text = pause_font.render("PAUSED", True, (255, 0, 0))

    win.blit(
        text,
        (
            WIN_WIDTH // 2 - text.get_width() // 2,
            WIN_HEIGHT // 2 - text.get_height() // 2,
        ),
    )

    pygame.display.update()


def reset_game(genomes):
    for g in genomes:
        g.fitness = 0.0
        g.adjusted_fitness = 0.0

    agents = [Agent(genome=g) for g in genomes]

    # Safety reset in case Agent objects are reused or changed later
    for agent in agents:
        agent.alive = True
        agent.frames_survived = 0
        agent.pipes_passed = 0

    base = Base(600)
    pipes = [Pipe(500)]
    score = 0
    return agents, base, pipes, score


async def run_generation(win, clock, genomes, generation, best_fitness_so_far):
    agents, base, pipes, score = reset_game(genomes)
    paused = False

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        if paused:
            draw_window(
                win,
                agents,
                pipes,
                base,
                score,
                generation,
                best_fitness_so_far,
            )

            draw_pause_text(win)

            await asyncio.sleep(0)
            continue

        alive_agents = [agent for agent in agents if agent.alive]
        if not alive_agents:
            break

        pipe_ind = 0
        if (
            len(pipes) > 1
            and alive_agents[0].bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
        ):
            pipe_ind = 1

        next_pipe = pipes[pipe_ind]

        # Move birds and count survival frames
        for agent in agents:
            if agent.alive:
                agent.think(next_pipe)
                agent.bird.move()
                agent.frames_survived += 1

        add_pipe = False
        removed_pipes = []

        for pipe in pipes:
            for agent in agents:
                if not agent.alive:
                    continue

                if pipe.collide(agent.bird):
                    agent.alive = False
                    continue

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
                    agent.pipes_passed += 1

        for rp in removed_pipes:
            if rp in pipes:
                pipes.remove(rp)

        for agent in agents:
            if agent.alive:
                if agent.bird.y + agent.bird.img.get_height() >= 600 or agent.bird.y < 0:
                    agent.alive = False

        # Continuously update displayed fitness using your formula
        if pipes:
            display_pipe = pipes[pipe_ind] if pipe_ind < len(pipes) else pipes[0]
            gap_center = display_pipe.height + display_pipe.GAP / 2
        else:
            gap_center = WIN_HEIGHT / 2

        for agent in agents:
            agent.genome.fitness = (
                agent.frames_survived
                + (agent.pipes_passed * 150)
                - (abs(agent.bird.y - gap_center) * 0.1)
            )
            agent.genome.fitness = max(0.0, agent.genome.fitness)

        base.move()

        current_best = max(agent.genome.fitness for agent in agents)
        draw_window(
            win,
            agents,
            pipes,
            base,
            score,
            generation,
            max(best_fitness_so_far, current_best),
        )

        await asyncio.sleep(0)

    # Final fitness calculation at generation end
    if pipes:
        final_pipe = pipes[0]
        gap_center = final_pipe.height + final_pipe.GAP / 2
    else:
        gap_center = WIN_HEIGHT / 2

    for agent in agents:
        agent.genome.fitness = (
            agent.frames_survived
            + (agent.pipes_passed * 150)
            - (abs(agent.bird.y - gap_center) * 0.1)
        )
        agent.genome.fitness = max(0.0, agent.genome.fitness)

    return [agent.genome for agent in agents]


async def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    population = Population(POPULATION_SIZE, elite_count=2)
    best_fitness_so_far = float("-inf")

    for generation in range(1, MAX_GENERATIONS + 1):
        finished_genomes = await run_generation(
            win, clock, population.genomes, generation, best_fitness_so_far
        )

        generation_best = max(g.fitness for g in finished_genomes)
        best_fitness_so_far = max(best_fitness_so_far, generation_best)

        print(f"Generation {generation} best fitness: {generation_best:.2f}")

        population.genomes = finished_genomes
        population.evolve()

    pygame.quit()


asyncio.run(main())