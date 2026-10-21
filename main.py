import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption("Project 3: Monster Ambush")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)
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

rewards = [10, 5, 8, 20]

key_map = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3}

MAX_ROUNDS = 10

def reset_game():
    return {
        "score": 0,
        "ai_score": 0,
        "ai_prediction": None,
        "points": 0,
        "ev_prediction": None,
        "round_number": 0,
        "current_state": random.randint(0, 3), # monster starts somewhere random
        "from_state": None,
        "ambush_state": None,
        "next_state": None,
        "message": "Press 1-4 to set your ambush!",
    }

def expected_rewards(state):
    expected = []
    for i in range(4):
        value = transition_matrix[state][i] * rewards[i]
        expected.append(value)
    return expected

def compare_strategies():
    totals = {"Random": 0, "Highest Probability": 0, "Highest Expected Reward": 0}
    state = random.randint(0, 3)
    for _ in range(100):
        next_state = random.choices(range(4), weights=transition_matrix[state], k=1)[0]

        random_pick = random.randint(0, 3)
        row = transition_matrix[state]
        prob_pick = row.index(max(row))
        expected = expected_rewards(state)
        ev_pick = expected.index(max(expected))

        if random_pick == next_state:
            totals["Random"] += rewards[next_state]
        if prob_pick == next_state:
            totals["Highest Probability"] += rewards[next_state]
        if ev_pick == next_state:
            totals["Highest Expected Reward"] += rewards[next_state]

        state = next_state

    print("100-round results (total reward):")
    for name in totals:
        print(f"  {name}: {totals[name]}")

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

                row = transition_matrix[game["current_state"]]
                game["ai_prediction"] = row.index(max(row))

                expected = expected_rewards(game["current_state"])
                game["ev_prediction"] = expected.index(max(expected))

                game["next_state"] = random.choices(
                    range(4),
                    weights=transition_matrix[game["current_state"]],
                    k=1
                )[0]

                reward = rewards[game["next_state"]]

                if game["ambush_state"] == game["next_state"]:
                    game["score"] += 1
                    game["points"] += reward
                    game["message"] = f"Ambush successful! +{reward} points (Total: {game['points']})"
                else:
                    game["message"] = f"The monster escaped! (Total: {game['points']})"

                if game["ai_prediction"] == game["next_state"]:
                    game["ai_score"] += 1

                game["current_state"] = game["next_state"]
                game["round_number"] += 1

            if event.key == pygame.K_r and game["round_number"] >= MAX_ROUNDS:
                game = reset_game()

            if event.key == pygame.K_s:
                compare_strategies()
                game["message"] = "100-round test done! Check your terminal."

    screen.fill((0, 0, 0))

    row = transition_matrix[game["current_state"]]
    for i in range(4):
        pygame.draw.rect(screen, colors[i], rects[i])
        label = font.render(f"{i + 1} = {states[i]}", True, (255, 255, 255))
        screen.blit(label, (rects[i].x + 15, rects[i].y + 15))
        reward_text = small_font.render(f"Reward: +{rewards[i]}", True, (255, 255, 255))
        screen.blit(reward_text, (rects[i].x + 15, rects[i].y + 50))
        chance_text = small_font.render(f"Chance: {row[i] * 100:.0f}%", True, (255, 255, 255))
        screen.blit(chance_text, (rects[i].x + 15, rects[i].y + 80))

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
        lines.append(f"AI Boss Would Ambush: {states[game['ai_prediction']]}")
        lines.append(f"Smart AI (Expected Reward) Would Ambush: {states[game['ev_prediction']]}")
        lines.append(f"Monster Moved To: {states[game['next_state']]}")
    lines.append(game["message"])
    lines.append(f"Human Prediction: {game['score']}/{game['round_number']}   AI Prediction: {game['ai_score']}/{game['round_number']}   (Round {game['round_number']} of {MAX_ROUNDS})")

    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (20, y))
        y += 32

    # game over message
    if game["round_number"] >= MAX_ROUNDS:
        if game["score"] > game["ai_score"]:
            winner = "You beat the AI!"
        elif game["score"] < game["ai_score"]:
            winner = "The AI wins!"
        else:
            winner = "It's a tie!"
        over = font.render(f"GAME OVER! {winner} (R = restart)", True, (255, 80, 80))
        screen.blit(over, (20, 855))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()