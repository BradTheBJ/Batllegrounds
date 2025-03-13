import os
import pygame
import sys
from pynput.mouse import Listener
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1980, 1080
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Movable Square")

# Define colors
black = "black"
white = 255, 255, 255  # White color for the hitbox
red = (255, 0, 0)

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
image_dir = os.path.dirname(__file__)  # Get the directory of the current script
right_walking_img_list = [pygame.transform.scale(pygame.image.load(os.path.join(image_dir, f"R{i}.png")), (square_size, square_size * 1.2)) for i in range(1, 10)]
left_walking_img_list = [pygame.transform.scale(pygame.image.load(os.path.join(image_dir, f"L{i}.png")), (square_size, square_size * 1.2)) for i in range(1, 10)]

player_frame = 0
animation_speed = 5
frame_count = 0

turn_right = True
turn_left = False

# Borders
left_border_x = 0
right_border_x = width - square_size

# Hit box properties
HitBoxWidth = 80  # Set hitbox width to 80
HitBoxHeight = square_size  # Set hitbox height to be equal to the player's height
HitBoxX = square_x
HitBoxY = square_y
hitbox_active = False
hitbox_start_time = 0

# Stun properties
stunned = False
stun_duration = 0.2  # Additional 0.2 seconds of stun after hitbox disappears

# Attack logic
def Attack():
    global square_x, hitbox_active, hitbox_start_time, HitBoxX
    # Spawn the hitbox in front of the player based on the direction
    if turn_right:
        HitBoxX = square_x + square_size  # Spawn to the right of the player
    else:
        HitBoxX = square_x - HitBoxWidth  # Spawn to the left of the player

    hitbox_active = True
    hitbox_start_time = time.time()  # Start the timer when the hitbox spawns

# Mouse click listener
def on_click(x, y, button, pressed):
    if pressed:
        Attack()

# Start listener for mouse clicks
listener = Listener(on_click=on_click)
listener.start()

WorldCuttingSlashWidth = 70
WorldCuttingSlashX = square_x
WorldCuttingSlashY = 0  # Start at the top of the screen
WorldCuttingSlashSpeed = 10
world_cutting_slash_active = False

def WolrdCuttingSlashMovement():
    global WorldCuttingSlashX, world_cutting_slash_active
    if not world_cutting_slash_active:
        WorldCuttingSlashX = square_x  # Set the initial position to the current square position
        world_cutting_slash_active = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False

    # Check if the player is stunned
    if stunned:
        if time.time() - stun_start_time > stun_duration:
            stunned = False  # Unstun the player after stun duration
        else:
            velocity = 0  # Stop movement during stun

    # If the hitbox is active, prevent movement
    if hitbox_active and time.time() - hitbox_start_time < 0.3:
        velocity = 0  # Disable movement while the hitbox is active
    elif not world_cutting_slash_active:  # Prevent movement if World Cutting Slash is active
        # Player movement logic (left-right)
        if not stunned:  # Only allow movement if not stunned
            if keys[pygame.K_a]:
                velocity = max(velocity - 0.5, -TerminalVelocity)
                turn_right = False
                turn_left = True
                moving = True
            elif keys[pygame.K_d]:
                velocity = min(velocity + 0.5, TerminalVelocity)
                turn_right = True
                turn_left = False
                moving = True
            else:
                velocity = 0  # Stop movement completely if no key is pressed

    # Jump logic
    if keys[pygame.K_SPACE] and not jumping and not world_cutting_slash_active:
        jumping = True
        jump_velocity = -Jump_Force  # Initial jump push

    if jumping:
        square_y += jump_velocity
        jump_velocity += Gravity
        if square_y >= 940:  # Land on the ground
            square_y = 940
            jumping = False

    # Horizontal movement
    square_x += velocity
    square_x = max(left_border_x, min(square_x, right_border_x))  # Stay in bounds

    # Handle player animation frames
    if moving:
        frame_count += 1
        if frame_count >= animation_speed:
            player_frame = (player_frame + 1) % 9
            frame_count = 0
    else:
        player_frame = 0

    # Deactivate hitbox after 0.3 seconds and stun player for 0.2 seconds
    if hitbox_active and time.time() - hitbox_start_time > 0.3:
        hitbox_active = False
        stunned = True
        stun_start_time = time.time()  # Start the stun timer

    if keys[pygame.K_g]:
        WolrdCuttingSlashMovement()

    # Update World Cutting Slash position
    if world_cutting_slash_active:
        if square_x <= 990:
            WorldCuttingSlashX += WorldCuttingSlashSpeed
        else:
            WorldCuttingSlashX -= WorldCuttingSlashSpeed
        if WorldCuttingSlashX >= right_border_x or WorldCuttingSlashX <= left_border_x:
            world_cutting_slash_active = False

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Rendering
    window.fill(black)

    # Draw the hitbox if it is active
    if hitbox_active:
        pygame.draw.rect(window, white, (HitBoxX, square_y, HitBoxWidth, HitBoxHeight))

    # Draw the player
    if turn_right:
        window.blit(right_walking_img_list[player_frame], (square_x, square_y))
    else:
        window.blit(left_walking_img_list[player_frame], (square_x, square_y))

    # Draw the World Cutting Slash if it is active
    if world_cutting_slash_active:
        pygame.draw.rect(window, red, (WorldCuttingSlashX, WorldCuttingSlashY, WorldCuttingSlashWidth, height))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()