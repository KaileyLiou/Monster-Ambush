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

colors = [(50, 50, 50), (40, 20, 90), (0, 100, 0), (255, 140, 0)]

key_map = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3}
 
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

game = reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in key_map and game["round_number"] < MAX_ROUNDS:
                game["ambush_state"] = key_map[event.key]
                game["from_state"] = game["current_state"]
 
                game["next_state"] = random.choices(
                    range(4),
                    weights=transition_matrix[game["current_state"]],
                    k=1
                )[0]

                if game["ambush_state"] == game["next_state"]:
                    game["score"] += 1
                    game["message"] = "Ambush successful!"
                else:
                    game["message"] = "The monster escaped!"
 
                game["current_state"] = game["next_state"]
                game["round_number"] += 1
 
            if event.key == pygame.K_r and game["round_number"] >= MAX_ROUNDS:
                game = reset_game()

    screen.fill((0, 0, 0))

    for i in range(4):
        pygame.draw.rect(screen, colors[i], rects[i])
        label = font.render(f"{i + 1} = {states[i]}", True, (255, 255, 255))
        screen.blit(label, (rects[i].x + 15, rects[i].y + 15))
 
    if game["ambush_state"] is not None:
        pygame.draw.rect(screen, (255, 0, 0), rects[game["ambush_state"]], 6)
 
    pygame.draw.circle(screen, (255, 255, 0), rects[game["current_state"]].center, 40)

    y = 620
    lines = []
    if game["round_number"] == 0:
        lines.append(f"Monster is in: {states[game['current_state']]}")
    else:
        lines.append(f"Current Location: {states[game['from_state']]}")
        lines.append(f"Your Ambush: {states[game['ambush_state']]}")
        lines.append(f"Monster Moved To: {states[game['next_state']]}")
    lines.append(game["message"])
    lines.append(f"Score: {game['score']} / {game['round_number']}   (Round {game['round_number']} of {MAX_ROUNDS})")
 
    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (20, y))
        y += 32
 
    # game over message
    if game["round_number"] >= MAX_ROUNDS:
        over = big_font.render(
            f"GAME OVER! Final score: {game['score']} / {MAX_ROUNDS}",
            f"Press R to play again",
            True, (255, 80, 80))
        screen.blit(over, (20, 750))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()