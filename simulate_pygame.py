import pygame
import sys

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# City data
cities = {
    'Mediterranean Avenue/Old Kent Rd': (50, 250),
    'Baltic Avenue/Whitechapel Rd': (250, 450),
    'Oriental Avenue/The Angel, Islington': (450, 250),
    'Vermont Avenue/Euston Rd': (250, 50)
}

players = {
    1: {'color': YELLOW, 'position': 'Mediterranean Avenue/Old Kent Rd'},
    2: {'color': RED, 'position': 'Mediterranean Avenue/Old Kent Rd'}
}


pass_data = [
    [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 1), ('Vermont Avenue/Euston Rd', 2)],
    [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 2), ('Vermont Avenue/Euston Rd', 2)],
    [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 2), ('Vermont Avenue/Euston Rd', 1)]
]


pygame.init()

WINDOW_SIZE = (500, 500)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Monopoly Simulation")


clock = pygame.time.Clock()

running = True
current_pass = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill(WHITE)

    
    for city, (x, y) in cities.items():
        pygame.draw.circle(screen, BLACK, (x, y), 5)
        text = pygame.font.SysFont(None, 20).render(city, True, BLACK)
        screen.blit(text, (x - text.get_width() / 2, y + 10))

    
    if current_pass < len(pass_data):
        for city, player in pass_data[current_pass]:
            players[player]['position'] = city
    print("I AM HEREEE")
    print(players)
    for player, data in players.items():
        x, y = cities[data['position']]
        pygame.draw.circle(screen, data['color'], (x, y), 10)


    pygame.display.flip()


    current_pass += 1
    if current_pass >= len(pass_data):
        current_pass = 0


    clock.tick(2)

pygame.quit()
sys.exit()
