import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1980, 1080
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Movable Square")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Define the square properties
square_size = 50
square_x = width // 2
square_y = height - square_size  # Position the square at the bottom of the screen
square_speed = 5

# Define the WorldCuttingSlash properties
WorldCuttingSlashSize = 70
WorldCuttingSlashX = square_x
WorldCuttingSlashY = height / 2
WorldCuttingSlashSpeed = 10

def WolrdCuttingSlashMovement():
    pygame.draw.rect(window, red, (WorldCuttingSlashX, WorldCuttingSlashY, WorldCuttingSlashSize, WorldCuttingSlashSize))
    while True:
        WorldCuttingSlashX += WorldCuttingSlashSpeed
        


# Define border objects properties
border_object_size = 50

# Define the invisible borders
left_border = pygame.Rect(0, 0, border_object_size, height)
right_border = pygame.Rect(width - border_object_size, 0, border_object_size, height)
top_border = pygame.Rect(0, 0, width, border_object_size)
bottom_border = pygame.Rect(0, height - border_object_size, width, border_object_size)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Move the square
    if keys[pygame.K_a]:
        square_x -= square_speed

    if keys[pygame.K_d]:
        square_x += square_speed

    # Ensure the square stays within the screen bounds
    if square_x < left_border.width:
        square_x = left_border.width
    if square_x > width - square_size - right_border.width:
        square_x = width - square_size - right_border.width

    # Fill the window with black
    window.fill(black)

    # Draw the square
    pygame.draw.rect(window, white, (square_x, square_y, square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()