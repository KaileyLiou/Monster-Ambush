import pygame
import math
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Project 3: Monster Ambush")
clock = pygame.time.Clock()

score = 0
ambush_state = random.randint(0, 3)
font = pygame.font.Font(None, 40)

states = [
    "Graveyard",
    "Haunted House",
    "Forest",
    "Pumpkin Patch"
]

pygame.draw.rect(screen, (50, 50, 50), (0, 0, 500, 400)) # graveyard (dark gray)
pygame.draw.rect(screen, (100, 100, 100), (500, 0, 500, 400)) # haunted house (dark blue)
pygame.draw.rect(screen, (0, 100, 0), (0, 400, 500, 400)) # forest (dark green)
pygame.draw.rect(screen, (255, 165, 0), (500, 400, 500, 400)) # pumpkin patch (orange)
pygame.draw.aaline(screen, (255, 255, 0), (250, 200), (250, 200), 50) # monster (yellow)

transition_matrix = [
    [0.10, 0.45, 0.30, 0.15],
    [0.35, 0.10, 0.40, 0.15],
    [0.25, 0.35, 0.15, 0.25],
    [0.40, 0.20, 0.20, 0.20]
]

current_state = 2

next_state = random.choices(
    range(4),
    weights=transition_matrix[current_state],
    k=1
)[0]

if ambush_state == next_state:
    score += 1
    message = "AMBUSH SUCCESSFUL!"
else:
    message = "The monster escaped!"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    state_text = font.render(f"Current State: {states[current_state]}", True, (255, 255, 255))
    screen.blit(state_text, (20, 20))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 60))

    message_text = font.render(message, True, (255, 0, 0))
    screen.blit(message_text, (20, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()