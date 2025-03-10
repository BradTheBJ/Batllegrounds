import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1980, 1080
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Movable Square")

# Define colors
black = "black"
red = "red"

# Player properties
square_size = 120
square_x = 300
square_y = 940
TerminalVelocity = 5
velocity = 0
Jump_Force = 25  # Max jump force per frame
Gravity = 2  # Gravity acceleration
jump_velocity = 0
jumping = False

# Load and scale images
right_walking_img_list = [pygame.transform.scale(pygame.image.load(f"R{i}.png"), (square_size, square_size * 1.2)) for i
                          in range(1, 10)]
left_walking_img_list = [pygame.transform.scale(pygame.image.load(f"L{i}.png"), (square_size, square_size * 1.2)) for i
                         in range(1, 10)]

player_frame = 0
animation_speed = 5
frame_count = 0

turn_right = True
turn_left = False

# WorldCuttingSlash properties
WorldCuttingSlashWidth = 70
WorldCuttingSlashSpeed = 10

# Borders
left_border_x = 0
right_border_x = width - square_size


def WorldCuttingSlashMovement():
    global square_x

    # Spawn in front of the player
    if turn_right:
        WorldCuttingSlashX = square_x + square_size  # Right side of player
    else:
        WorldCuttingSlashX = square_x - WorldCuttingSlashWidth  # Left side of player

    while True:
        WorldCuttingSlashX += WorldCuttingSlashSpeed if turn_right else -WorldCuttingSlashSpeed
        window.fill(black)

        if turn_right:
            window.blit(right_walking_img_list[player_frame], (square_x, square_y))
        else:
            window.blit(left_walking_img_list[player_frame], (square_x, square_y))

        pygame.draw.rect(window, red, (WorldCuttingSlashX, 0, WorldCuttingSlashWidth, height))
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        if WorldCuttingSlashX >= right_border_x or WorldCuttingSlashX <= left_border_x:
            break


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Movement logic
    if keys[pygame.K_a]:
        if velocity > -TerminalVelocity:
            velocity -= 0.5
        turn_right = False
        turn_left = True
        moving = True

    elif keys[pygame.K_d]:
        if velocity < TerminalVelocity:
            velocity += 0.5
        turn_right = True
        turn_left = False
        moving = True

    else:
        velocity = 0  # Stop movement completely if no key is pressed

    # Jump logic
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
        jump_velocity = -Jump_Force  # Initial jump push

    if jumping:
        square_y += jump_velocity  # Apply jump velocity
        jump_velocity += Gravity  # Apply gravity
        if square_y >= 940:  # Land on the ground
            square_y = 940
            jumping = False

    # Horizontal movement
    square_x += velocity
    square_x = max(left_border_x, min(square_x, right_border_x))  # Stay in bounds

    # Trigger WorldCuttingSlash
    if keys[pygame.K_g]:
        WorldCuttingSlashMovement()

    # Control animation frame timing
    if moving:
        frame_count += 1
        if frame_count >= animation_speed:
            player_frame = (player_frame + 1) % 9
            frame_count = 0
    else:
        player_frame = 0

    # Rendering
    window.fill(black)
    if turn_right:
        window.blit(right_walking_img_list[player_frame], (square_x, square_y))
    else:
        window.blit(left_walking_img_list[player_frame], (square_x, square_y))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
