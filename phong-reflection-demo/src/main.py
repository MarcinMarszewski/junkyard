import pygame
import sys
from phong import PhongModel
from utils import normalize

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
BALL_COLOR = (255, 255, 255)
LIGHT_POSITION = (400, 100)
VIEWER_POSITION = (400, 300)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phong Reflection Demo")

# Create a Phong model instance
phong_model = PhongModel([0.0, 0.5, 0.5], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0], 32)

def draw_ball(surface, position, radius):
    # Calculate light reflection using Phong model
    normal = normalize((position[0] - LIGHT_POSITION[0], position[1] - LIGHT_POSITION[1], 0.0))
    diffuse = phong_model.calculate_diffuse(normal, LIGHT_POSITION)
    specular = phong_model.calculate_specular(normal, VIEWER_POSITION)
    ambient = phong_model.calculate_ambient()

    # Combine the colors
    color = (
        min(BALL_COLOR[0] * (ambient + diffuse + specular), 255),
        min(BALL_COLOR[1] * (ambient + diffuse + specular), 255),
        min(BALL_COLOR[2] * (ambient + diffuse + specular), 255)
    )

    pygame.draw.circle(surface, color, position, radius)

def main():
    clock = pygame.time.Clock()
    ball_position = (400, 300)
    ball_radius = 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)
        draw_ball(screen, ball_position, ball_radius)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()