import pygame
import random
import sys
import os
# Inicjalizacja Pygame
pygame.init()

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Ustawienia ekranu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bobiki: Zamek i Fortece")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (105, 105, 105)

# Czcionki
font = pygame.font.Font(None, 36)

# Grafiki
castle_img = pygame.image.load(os.path.join(ASSETS_DIR, "castle.png"))
fortress_img = pygame.image.load(os.path.join(ASSETS_DIR, "fortress.png"))
zombie_img = pygame.image.load(os.path.join(ASSETS_DIR, "zombie.png"))
orc_img = pygame.image.load(os.path.join(ASSETS_DIR, "orc.png"))
player_img = pygame.image.load(os.path.join(ASSETS_DIR, "player.png"))
boss_img = pygame.image.load(os.path.join(ASSETS_DIR, "boss.png"))
coin_img = pygame.image.load(os.path.join(ASSETS_DIR, "coin.png"))
sword_img = pygame.image.load(os.path.join(ASSETS_DIR, "sword.png"))

# Skalowanie grafik
castle_img = pygame.transform.scale(castle_img, (200, 200))
fortress_img = pygame.transform.scale(fortress_img, (150, 150))
zombie_img = pygame.transform.scale(zombie_img, (50, 50))
orc_img = pygame.transform.scale(orc_img, (60, 60))
player_img = pygame.transform.scale(player_img, (50, 50))
boss_img = pygame.transform.scale(boss_img, (100, 100))
coin_img = pygame.transform.scale(coin_img, (30, 30))
sword_img = pygame.transform.scale(sword_img, (40, 40))

# Pozycje
castle_pos = (WIDTH // 2 - 100, HEIGHT // 2 - 200)
fortress_pos = [(200, 300), (400, 400), (600, 200)]
player_pos = [WIDTH // 2, HEIGHT // 2]
player_health = 20
player_coins = 0
player_damage = 5

# Wrogowie
enemies = [
    {"type": "zombie", "health": 10, "damage": 3, "position": (250, 350)},
    {"type": "orc", "health": 20, "damage": 5, "position": (500, 450)},
]
boss = {"type": "mag", "health": 50, "damage": 10, "position": (WIDTH // 2 - 50, 100)}

# Status gry
game_phase = "explore"  # "explore", "fight", "fortress_boss", "castle_tasks", "game_over"
current_task = None
task_completed = False

# Funkcje
def draw_text(text, x, y, color=WHITE):
    """Wyświetlanie tekstu na ekranie."""
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_castle():
    """Rysowanie zamku."""
    screen.blit(castle_img, castle_pos)
    draw_text("Zamek: Kliknij, aby wejść", castle_pos[0], castle_pos[1] - 30)

def draw_fortresses():
    """Rysowanie fortec."""
    for pos in fortress_pos:
        screen.blit(fortress_img, pos)
    draw_text("Fortece: Kliknij, aby walczyć", 10, 10)

def draw_player():
    """Rysowanie gracza."""
    screen.blit(player_img, player_pos)

def draw_enemies():
    """Rysowanie wrogów."""
    for enemy in enemies:
        if enemy["type"] == "zombie":
            screen.blit(zombie_img, enemy["position"])
        elif enemy["type"] == "orc":
            screen.blit(orc_img, enemy["position"])
    if game_phase == "fortress_boss":
        screen.blit(boss_img, boss["position"])

def handle_fight():
    """Obsługa walki z przeciwnikami."""
    global enemies, player_health, game_phase
    for enemy in enemies:
        if random.random() < 0.5:  # 50% szans na atak
            player_health -= enemy["damage"]
        enemy["health"] -= player_damage
        if enemy["health"] <= 0:
            enemies.remove(enemy)
            global player_coins
            player_coins += 10  # Nagroda za zabicie
    if player_health <= 0:
        game_phase = "game_over"
    if not enemies:  # Wszystkie pokonane
        game_phase = "fortress_boss"

def fight_boss():
    """Walka z bossem."""
    global boss, player_health, player_coins, game_phase
    player_health -= boss["damage"]
    boss["health"] -= player_damage
    if boss["health"] <= 0:
        draw_text("Pokonałeś bossa! Gratulacje!", WIDTH // 2 - 100, HEIGHT // 2 - 50)
        player_coins += 50  # Nagroda
        game_phase = "explore"

def upgrade_weapon():
    """Ulepszanie broni w zamku."""
    global player_damage, player_coins
    if player_coins >= 20:
        player_damage += 5
        player_coins -= 20
        return "Broń ulepszona!"
    return "Za mało monet!"

# Główna pętla gry
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_phase == "explore" and castle_pos[0] <= x <= castle_pos[0] + 200 and castle_pos[1] <= y <= castle_pos[1] + 200:
                game_phase = "castle_tasks"
            for fortress in fortress_pos:
                if fortress[0] <= x <= fortress[0] + 150 and fortress[1] <= y <= fortress[1] + 150:
                    game_phase = "fight"
        if event.type == pygame.KEYDOWN:
            if game_phase == "castle_tasks" and event.key == pygame.K_u:
                message = upgrade_weapon()
                print(message)

    # Fazy gry
    if game_phase == "explore":
        draw_castle()
        draw_fortresses()
        draw_player()
        draw_text(f"Zdrowie: {player_health}", 10, HEIGHT - 70)
        draw_text(f"Monety: {player_coins}", 10, HEIGHT - 40)

    elif game_phase == "fight":
        draw_enemies()
        handle_fight()

    elif game_phase == "fortress_boss":
        draw_enemies()
        fight_boss()

    elif game_phase == "castle_tasks":
        draw_text("W zamku: Naciśnij U, aby ulepszyć broń", 10, 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
