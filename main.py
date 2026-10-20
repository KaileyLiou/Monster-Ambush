import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Project 3: Monster Ambush")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 48)

states = ["Graveyard", "Haunted House", "Forest", "Pumpkin Patch"]
transition_matrix = [
    [0.10, 0.45, 0.30, 0.15],
    [0.35, 0.10, 0.40, 0.15],
    [0.25, 0.35, 0.15, 0.25],
    [0.40, 0.20, 0.20, 0.20]
]

rects = [
    pygame.Rect(0, 0, 500, 300), # graveyard
    pygame.Rect(500, 0, 500, 300), # haunted house
    pygame.Rect(0, 300, 500, 300), # forest
    pygame.Rect(500, 300, 500, 300), # pumpkin patch
]

colors = [
    (50, 50, 50),
    (40, 20, 90),
    (0, 100, 0),
    (255, 140, 0),
]

key_map = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
}
 
MAX_ROUNDS = 10

def reset_game():
    return {
        "score": 0,
        "round_number": 0,
        "current_state": random.randint(0, 3), # monster starts somewhere random
        "from_state": None,
        "ambush_state": None,
        "next_state": None,
        "message": "Press 1-4 to set your ambush!",
    }

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

    game = reset_game()

    score = 0
    ambush_state = random.randint(0, 3)

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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()