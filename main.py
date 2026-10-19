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
