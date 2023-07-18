import pygame
import random

# Background of window
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Objects
ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

# Objects movement
MOVEMENTS = ["up", "down", "left", "right"]

# speed of object
OBJECT_SPEED = 5

# pygame start
pygame.init()

# Window Dimension
WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 700

# Window Creation
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Simulation")

# Images of Object
rock_image = pygame.image.load("rock.png")
paper_image = pygame.image.load("paper.png")
scissors_image = pygame.image.load("scissors.png")

# Object size
object_size = (40, 40)

# Makes all object size same
rock_image = pygame.transform.scale(rock_image, object_size)
paper_image = pygame.transform.scale(paper_image, object_size)
scissors_image = pygame.transform.scale(scissors_image, object_size)

# initial positions, speed, and types of the objects
objects = []
num_objects_per_side = 5 # number of objects per side
spacing = 100  # spacing between objects

for i in range(-num_objects_per_side, num_objects_per_side + 1):
    for j in range(-num_objects_per_side, num_objects_per_side + 1):
        object_type = random.choice([ROCK, PAPER, SCISSORS])
        object_position = [
            random.randint(object_size[0] // 2, WINDOW_WIDTH - object_size[0] // 2),
            random.randint(object_size[1] // 2, WINDOW_HEIGHT // 2 - object_size[1] // 2),
        ]
        object_velocity = [random.choice([-1, 1]), random.choice([-1, 1])]
        objects.append({"type": object_type, "position": object_position, "velocity": object_velocity})


# Function to move objects
def move_object(object_data):
    object_data["position"][0] += object_data["velocity"][0] * OBJECT_SPEED
    object_data["position"][1] += object_data["velocity"][1] * OBJECT_SPEED

    if object_data["position"][0] < 0:
        object_data["position"][0] = 0
        object_data["velocity"][0] *= -1
    elif object_data["position"][0] > WINDOW_WIDTH - object_size[0]:
        object_data["position"][0] = WINDOW_WIDTH - object_size[0]
        object_data["velocity"][0] *= -1

    if object_data["position"][1] < 0:
        object_data["position"][1] = 0
        object_data["velocity"][1] *= -1
    elif object_data["position"][1] > WINDOW_HEIGHT - object_size[1]:
        object_data["position"][1] = WINDOW_HEIGHT - object_size[1]
        object_data["velocity"][1] *= -1

# Function to check collision
def check_collision(object_data1, object_data2):
    object_position1 = object_data1["position"]
    object_position2 = object_data2["position"]

    dx = object_position1[0] - object_position2[0]
    dy = object_position1[1] - object_position2[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance < object_size[0]:
        return True
    else:
        return False

# Function to change object on collision
def update_objects(objects):
    updated_objects = []
    for i in range(len(objects)):
        object_data = objects[i]
        object_type = object_data["type"]
        object_position = object_data["position"]
        object_velocity = object_data["velocity"]
        updated_type = object_type  # Store the updated type
        for j in range(len(objects)):
            if j != i:  # Exclude self-check
                if check_collision(object_data, objects[j]):
                    other_type = objects[j]["type"]
                    if (object_type == ROCK and other_type == PAPER) or (object_type == PAPER and other_type == SCISSORS) or (object_type == SCISSORS and other_type == ROCK):
                        # Assign the other type if the current object loses the collision
                        updated_type = other_type
                        break
        updated_objects.append({"type": updated_type, "position": object_position, "velocity": object_velocity})
    return updated_objects

# Function to check for winner
def check_winner(objects):
    object_types = set([object_data["type"] for object_data in objects])
    if len(object_types) == 1:
        return object_types.pop()
    else:
        return None

# Position of 2 Botton
button_y = WINDOW_HEIGHT - int(0.1 * WINDOW_HEIGHT)

# Function for restart button 
def draw_restart_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Again", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2 - 100, button_y))
    pygame.draw.rect(window, BLACK, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    window.blit(text, text_rect)
    return text_rect

# Function for Exit Button
def draw_exit_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Exit", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2 + 100, button_y))
    pygame.draw.rect(window, BLACK, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    window.blit(text, text_rect)
    return text_rect

# For restarting Game
def restart_game():
    global objects
    objects = []
    for _ in range(num_objects_per_side * num_objects_per_side):
        object_type = random.choice([ROCK, PAPER, SCISSORS])
        object_position = [
            random.randint(object_size[0] // 2, WINDOW_WIDTH - object_size[0] // 2),
            random.randint(object_size[1] // 2, WINDOW_HEIGHT - object_size[1] // 2),
        ]
        object_velocity = [random.choice([-1, 1]), random.choice([-1, 1])]
        objects.append({"type": object_type, "position": object_position, "velocity": object_velocity})



# Game iteration
running = True
clock = pygame.time.Clock()
winner = None
restart = False
exit_game = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if winner and restart:
                if restart_button_rect.collidepoint(event.pos):
                    restart_game()
                    winner = None
                    restart = False
                elif exit_button_rect.collidepoint(event.pos):
                    exit_game = True

    if not winner:
        for object_data in objects:
            move_object(object_data)

        objects = update_objects(objects)
        winner = check_winner(objects)

    window.fill(BLACK)

    for object_data in objects:
        object_type = object_data["type"]
        object_position = object_data["position"]

        if object_type == ROCK:
            window.blit(rock_image, object_position)
        elif object_type == PAPER:
            window.blit(paper_image, object_position)
        elif object_type == SCISSORS:
            window.blit(scissors_image, object_position)

    # For winner announcement
    if winner:
        pygame.draw.rect(window, WHITE, (0, 0, WINDOW_WIDTH, 60))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Winner: {winner.capitalize()}", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        window.blit(text, text_rect)

        # Button after winner Announcement
        pygame.draw.rect(window, WHITE, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
        restart_button_rect = draw_restart_button()
        exit_button_rect = draw_exit_button()

        restart = True

    # Window restart
    pygame.display.flip()

    if exit_game:
        break

    # FPS
    clock.tick(60)

pygame.quit()
