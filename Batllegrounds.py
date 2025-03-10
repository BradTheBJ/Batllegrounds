import pygame
import sys
from pynput.mouse import Listener
import time  # To track the time for disabling player movement

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1980, 1080
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Movable Square")

# Define colors
black = "black"
white = 255, 255, 255  # White color for the hitbox

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
right_walking_img_list = [pygame.transform.scale(pygame.image.load(f"R{i}.png"), (square_size, square_size * 1.2)) for i in range(1, 10)]
left_walking_img_list = [pygame.transform.scale(pygame.image.load(f"L{i}.png"), (square_size, square_size * 1.2)) for i in range(1, 10)]

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
stun_start_time = 0
stun_duration = 0.2  # Additional 0.2 seconds of stun after hitbox disappears

def Attack():
    global square_x, hitbox_active, hitbox_start_time, HitBoxX

    # Spawn the hitbox in front of the player based on the direction
    if turn_right:
        HitBoxX = square_x + square_size  # Spawn to the right of the player
    else:
        HitBoxX = square_x - HitBoxWidth  # Spawn to the left of the player

    hitbox_active = True
    hitbox_start_time = time.time()  # Start the timer when the hitbox spawns

def on_click(x, y, button, pressed):
    if pressed:
        Attack()

# Start listener for mouse clicks
listener = Listener(on_click=on_click)
listener.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False

    # Check if the player is stunned
    if stunned:
        # If the stun duration has passed, allow movement again
        if time.time() - stun_start_time > stun_duration:
            stunned = False
        else:
            velocity = 0  # Stop movement during stun

    # Disable movement if hitbox is active and time has not passed
    if hitbox_active and time.time() - hitbox_start_time < 0.3:
        velocity = 0  # Disable movement while the hitbox is active
    else:
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
        jump_velocity = -Jump_Force

    if jumping:
        square_y += jump_velocity
        jump_velocity += Gravity
        if square_y >= 940:
            square_y = 940
            jumping = False

    # Horizontal movement
    square_x += velocity
    square_x = max(left_border_x, min(square_x, right_border_x))

    # Control animation frame timing
    if moving:
        frame_count += 1
        if frame_count >= animation_speed:
            player_frame = (player_frame + 1) % 9
            frame_count = 0
            
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    else:
        player_frame = 0

    # Rendering
    window.fill(black)

    # Draw the hitbox if it is active
    if hitbox_active:
        pygame.draw.rect(window, white, (HitBoxX, square_y, HitBoxWidth, HitBoxHeight))  # White hitbox

    # Draw the player
    if turn_right:
        window.blit(right_walking_img_list[player_frame], (square_x, square_y))
    else:
        window.blit(left_walking_img_list[player_frame], (square_x, square_y))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # After 0.3 seconds, deactivate the hitbox and apply stun
    if hitbox_active and time.time() - hitbox_start_time > 0.3:
        hitbox_active = False
        stunned = True
        stun_start_time = time.time()  # Start the stun timer

pygame.quit()
sys.exit()
