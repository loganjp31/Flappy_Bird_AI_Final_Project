import asyncio
import os
import pygame

from Bird import Bird
from Pipe import Pipe
from Base import Base

pygame.init()
pygame.font.init()
pygame.display.set_caption("Flappy Bird")

WIN_WIDTH = 400
WIN_HEIGHT = 700

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "images")

BASE_IMG = pygame.transform.scale_by(
    pygame.image.load(os.path.join(IMG_DIR, "base.png")), 1.5
)
BG_IMG = pygame.transform.scale_by(
    pygame.image.load(os.path.join(IMG_DIR, "bg.png")), 1.5
)

STAT_FONT = pygame.font.SysFont("comicsans", 25)
GAMEOVER_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, bird, pipes, base, score, gameover):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)

    if gameover:
        text = GAMEOVER_FONT.render("GAME OVER", True, (0, 0, 0))
        win.blit(text, ((WIN_WIDTH - text.get_width()) // 2, WIN_HEIGHT // 2 - 50))

        text = STAT_FONT.render("Press R to Restart", True, (0, 0, 0))
        win.blit(text, ((WIN_WIDTH - text.get_width()) // 2, WIN_HEIGHT // 2 + 10))

    pygame.display.flip()


def reset_game():
    bird = Bird(150, 300)
    base = Base(600)
    pipes = [Pipe(500)]
    score = 0
    gameover = False
    paused = False
    return bird, base, pipes, score, gameover, paused


async def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    bird, base, pipes, score, gameover, paused = reset_game()
    run = True

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not paused:
                    bird.jump()
                elif event.key == pygame.K_r and paused:
                    bird, base, pipes, score, gameover, paused = reset_game()

        if not paused:
            bird.move()
            add_pipe = False
            removed_pipes = []

            for pipe in pipes:
                if pipe.collide(bird):
                    gameover = True
                    paused = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    removed_pipes.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(450))

            for rp in removed_pipes:
                if rp in pipes:
                    pipes.remove(rp)

            if bird.y + bird.img.get_height() >= 600 or bird.y < 0:
                gameover = True
                paused = True

            base.move()

        draw_window(win, bird, pipes, base, score, gameover)

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())