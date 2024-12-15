import pygame
import random
import sys
import os
# Inicjalizacja Pygame
pygame.init() 

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Load music
pygame.mixer.init(44100, -16, 2, 2048)  # Initialize with specific parameters
try:
    # Try loading .wav or .ogg instead of .m4a
    explore_music = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "music/explore.wav"))  # or .ogg
    explore_music.set_volume(0.1)  # Set volume to 50%

    # Load footsteps sound
    footsteps_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "music/player/footsteps.mp3"))
    footsteps_sound.set_volume(0.6)  # Set volume to 30%
except pygame.error as e:
    print(f"Couldn't load music: {e}")
    explore_music = None
    footsteps_sound = None

# At the top with other sound loads
try:
    hit_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "music/hit.wav"))
    hit_sound.set_volume(0.3)
except pygame.error as e:
    print(f"Couldn't load hit sound: {e}")
    hit_sound = None

# Add this with other sound loads at the top
try:
    sword_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "music/sword.wav"))
    sword_sound.set_volume(0.4)  # Adjust volume as needed
except pygame.error as e:
    print(f"Couldn't load sword sound: {e}")
    sword_sound = None

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


# Game states
WELCOME_SCREEN = "welcome"
EXPLORE = "explore"
FIGHT = "fight"
FORTRESS_BOSS = "fortress_boss"
CASTLE_TASKS = "castle_tasks"
GAME_OVER = "game_over"
GAME_WON = "game_won"

# Czcionki
font = pygame.font.Font(None, 36)

# Grafiki
castle_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/castle.png"))
background_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/background.png"))
fortress_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/fortress.png"))
zombie_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/zombie.png"))
orc_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/orc.png"))
player_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/player3.png"))
boss_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/boss.png"))
coin_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/coin.png"))
sword_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/sword.png"))

# Skalowanie grafik
castle_img = pygame.transform.scale(castle_img, (200, 200))
fortress_img = pygame.transform.scale(fortress_img, (150, 150))
zombie_img = pygame.transform.scale(zombie_img, (50, 50))
orc_img = pygame.transform.scale(orc_img, (60, 60))
player_img = pygame.transform.scale(player_img, (50, 50))
boss_img = pygame.transform.scale(boss_img, (100, 100))
coin_img = pygame.transform.scale(coin_img, (30, 30))
sword_img = pygame.transform.scale(sword_img, (40, 40))
# Add this with other image loads
heart_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/heart.png"))
heart_img = pygame.transform.scale(heart_img, (30, 30))  # Adjust size as needed

dragon_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/dragon.png"))
fireball_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/fireball.png"))  # You'll need a fireball image

# Scale images
dragon_img = pygame.transform.scale(dragon_img, (200, 200))
fireball_img = pygame.transform.scale(fireball_img, (60, 60))

# Dragon properties
dragon_rect = dragon_img.get_rect()
dragon_rect.x = WIDTH - 200  # Place dragon on the right side
dragon_rect.y = 100
dragon_speed = 3
dragon_direction = 1  # 1 for down, -1 for up

# Add this with other image loads
dragon_heart_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/dragon-heart.png"))
dragon_heart_img = pygame.transform.scale(dragon_heart_img, (30, 30))  # Adjust size as needed

# Dragon properties
dragon_rect = dragon_img.get_rect()
dragon_rect.x = WIDTH - 200  # Place dragon on the right side
dragon_rect.y = 100
dragon_speed = 3
dragon_direction = 1  # 1 for down, -1 for up
dragon_health = 5  # Add this line - dragon starts with 5 health points

# Fireball properties
fireballs = []
FIREBALL_SPEED = 10
last_fireball_time = 0
FIREBALL_DELAY = random.randint(1000, 2000)  # Random delay between 1 and 2 seconds

# Pozycje
castle_pos = (WIDTH // 2 - 100, HEIGHT // 2 - 200)
fortress_pos = [(200, 300), (400, 400), (600, 200)]
# player_pos = [WIDTH // 2, HEIGHT // 2]
player_health = 20
player_coins = 0
player_damage = 5

# Dodaj po inicjalizacji zmiennych
PLAYER_SPEED = 5
player_rect = player_img.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)
# After loading player_img
player_img_right = pygame.transform.scale(player_img, (150, 150))  # Original facing right
player_img_left = pygame.transform.flip(player_img_right, True, False)  # Flipped version for left
player_facing_left = False  # Track which direction player is facing
player_lives = 3  # Start with 3 lives

is_moving = False
footsteps_timer = 0
FOOTSTEPS_DELAY = 300  # Delay between footsteps sounds in milliseconds

# Wrogowie
enemies = [
    {"type": "zombie", "health": 10, "damage": 3, "position": (250, 350)},
    {"type": "orc", "health": 20, "damage": 5, "position": (500, 450)},
]
boss = {"type": "mag", "health": 50, "damage": 10, "position": (WIDTH // 2 - 50, 100)}

# Status gry
# Change initial game_phase to WELCOME_SCREEN
game_phase = WELCOME_SCREEN
current_task = None
task_completed = False

background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# At the top with other initializations
footsteps_channel = None
if footsteps_sound:
    footsteps_channel = pygame.mixer.Channel(1)  # Use a dedicated channel for footsteps
    footsteps_sound.set_volume(0.3)  # Adjust volume (0.0 to 1.0)
    FOOTSTEPS_DELAY = 300  # Adjust delay between steps (in milliseconds)


def draw_victory_screen():
    """Display victory screen with final score."""
    # Create dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(192)
    screen.blit(overlay, (0, 0))
    
    # Draw "You Won!" text
    title_font = pygame.font.Font(None, 74)
    victory_text = title_font.render("YOU WON!", True, GREEN)
    victory_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(victory_text, victory_rect)
    
    # Draw final score
    stats_font = pygame.font.Font(None, 36)
    coins_text = stats_font.render(f"Final Score: {player_coins} coins", True, WHITE)
    coins_rect = coins_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(coins_text, coins_rect)
    
    # Draw play again button
    restart_text = font.render("Click to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
    screen.blit(restart_text, restart_rect)
    
    return restart_rect  # Return the rectangle for click detection

def draw_dragon_hearts():
    """Display dragon health as hearts."""
    heart_spacing = 35  # Space between hearts
    start_x = WIDTH - (heart_spacing * dragon_health) - 10
    start_y = 10
    
    for i in range(dragon_health):
        screen.blit(dragon_heart_img, (start_x + (i * heart_spacing), start_y))

def draw_game_over_screen():
    """Display game over screen with restart button."""
    # Create dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(192)  # More opaque than welcome screen
    screen.blit(overlay, (0, 0))
    
    # Draw "Game Over" text
    title_font = pygame.font.Font(None, 74)
    game_over_text = title_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(game_over_text, game_over_rect)
    
    # Draw score/stats
    stats_font = pygame.font.Font(None, 36)
    coins_text = stats_font.render(f"Coins collected: {player_coins}", True, WHITE)
    coins_rect = coins_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(coins_text, coins_rect)
    
    # Draw restart button
    restart_text = font.render("Click to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
    screen.blit(restart_text, restart_rect)
    
    return restart_rect  # Return the rectangle for click detection

def move_dragon():
    """Move the dragon up and down"""
    global dragon_direction
    
    dragon_rect.y += dragon_speed * dragon_direction
    
    # Change direction when reaching screen boundaries
    if dragon_rect.bottom >= HEIGHT:
        dragon_direction = -1
    elif dragon_rect.top <= 0:
        dragon_direction = 1

def shoot_fireball():
    """Create a new fireball"""
    fireball = pygame.Rect(dragon_rect.left, 
                          dragon_rect.centery, 
                          30, 30)  # adjust size as needed
    fireballs.append(fireball)

def update_fireballs():
    """Update fireball positions and remove ones that are off screen"""
    for fireball in fireballs[:]:  # Create a copy of the list to modify while iterating
        fireball.x -= FIREBALL_SPEED
        if fireball.right < 0:
            fireballs.remove(fireball)

def draw_dragon_and_fireballs():
    """Draw the dragon, its hearts, and all active fireballs"""
    screen.blit(dragon_img, dragon_rect)
    draw_dragon_hearts()  # Add this line
    for fireball in fireballs:
        screen.blit(fireball_img, fireball)

def draw_player():
    """Rysowanie gracza."""
    screen.blit(player_img, player_rect)
    
def draw_lives():
    """Display player lives as hearts."""
    heart_spacing = 35  # Space between hearts
    start_x = 10  # Starting x position
    start_y = 10  # Y position
    
    for i in range(player_lives):
        screen.blit(heart_img, (start_x + (i * heart_spacing), start_y))

# Add this function to draw welcome screen
def draw_welcome_screen():
    """Display welcome screen with start button."""
    # Draw castle as background
    screen.blit(pygame.transform.scale(castle_img, (WIDTH, HEIGHT)), (0, 0))
    
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Draw game title
    title_font = pygame.font.Font(None, 74)
    title_text = title_font.render("Bobik walczy ze smokiem", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(title_text, title_rect)
    
    # Draw start button
    start_text = font.render("Kliknij, aby rozpocząć grę", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
    screen.blit(start_text, start_rect)
    
    return start_rect  # Return the rectangle for click detection

def reset_game():
    """Reset all game variables to their initial states."""
    global player_health, player_coins, player_damage, player_lives, game_phase, dragon_health
    global player_rect, enemies, boss, fireballs
    
    # Reset player stats
    player_health = 20
    player_coins = 0
    player_damage = 5
    player_lives = 3
    dragon_health = 5
    # Reset player position
    player_rect.center = (WIDTH // 2, HEIGHT // 2)
    
    # Reset enemies
    enemies = [
        {"type": "zombie", "health": 10, "damage": 3, "position": (250, 350)},
        {"type": "orc", "health": 20, "damage": 5, "position": (500, 450)},
    ]
    
    # Reset boss
    boss = {"type": "mag", "health": 50, "damage": 10, "position": (WIDTH // 2 - 50, 100)}
    
    # Clear fireballs
    fireballs.clear()
    
    # Reset game phase
    game_phase = EXPLORE
    
    # Reset music
    if explore_music:
        explore_music.stop()  # Stop any currently playing music
        try:
            explore_music.play(-1)  # Restart the music
        except pygame.error as e:
            print(f"Couldn't restart music: {e}")

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
    if player_facing_left:
        screen.blit(player_img_left, player_rect)
    else:
        screen.blit(player_img_right, player_rect)

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
    global enemies, player_health, game_phase, player_lives
    for enemy in enemies:
        if random.random() < 0.5:  # 50% szans na atak
            player_health -= enemy["damage"]
        enemy["health"] -= player_damage
        if enemy["health"] <= 0:
            enemies.remove(enemy)
            global player_coins
            player_coins += 10  # Nagroda za zabicie
    if player_health <= 0:
        player_lives -= 1  # Decrease lives when health reaches 0
        if player_lives <= 0:
            game_phase = GAME_OVER  # Only game over when all lives are lost
        else:
            player_health = 20  # Reset health when losing a life
    if not enemies:  # Wszystkie pokonane
        game_phase = "fortress_boss"

def draw_sword_swing():
    """Draw a simple sword swing animation"""
    swing_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
    if player_facing_left:
        pygame.draw.arc(swing_surface, (255, 255, 255, 128), 
                       (0, 0, 100, 100), 0, 3.14, 3)
        screen.blit(swing_surface, 
                   (player_rect.left - 50, player_rect.centery - 50))
    else:
        pygame.draw.arc(swing_surface, (255, 255, 255, 128), 
                       (0, 0, 100, 100), 3.14, 6.28, 3)
        screen.blit(swing_surface, 
                   (player_rect.right - 50, player_rect.centery - 50))
        
def draw_game_over_screen():
    """Display game over screen with restart button."""
    # Create dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(192)  # More opaque than welcome screen
    screen.blit(overlay, (0, 0))
    
    # Draw "Game Over" text
    title_font = pygame.font.Font(None, 74)
    game_over_text = title_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(game_over_text, game_over_rect)
    
    # Draw score/stats
    stats_font = pygame.font.Font(None, 36)
    coins_text = stats_font.render(f"Coins collected: {player_coins}", True, WHITE)
    coins_rect = coins_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(coins_text, coins_rect)
    
    # Draw restart button
    restart_text = font.render("Click to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
    screen.blit(restart_text, restart_rect)
    
    return restart_rect  # Return the rectangle for click detection

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

            if game_phase == WELCOME_SCREEN:
                start_rect = draw_welcome_screen()
                if start_rect.collidepoint(x, y):
                    game_phase = EXPLORE
                    if explore_music:
                        try:
                            explore_music.play(-1)  # -1 means loop indefinitely
                        except pygame.error as e:
                            print(f"Couldn't play music: {e}")

                
            # Ograniczenie ruchu do granic ekranu
            player_rect.clamp_ip(screen.get_rect())
            if game_phase == WELCOME_SCREEN:
                start_rect = draw_welcome_screen()
                if start_rect.collidepoint(x, y):
                    game_phase = EXPLORE

            if game_phase == GAME_OVER:
                restart_rect = draw_game_over_screen()
                if restart_rect.collidepoint(x, y):
                    reset_game()
                    if explore_music:
                        try:
                            explore_music.play(-1)
                        except pygame.error as e:
                            print(f"Couldn't play music: {e}")

            if game_phase == GAME_WON:
                restart_rect = draw_victory_screen()
                if restart_rect.collidepoint(x, y):
                    reset_game()
                    if explore_music:
                        try:
                            explore_music.play(-1)
                        except pygame.error as e:
                            print(f"Couldn't play music: {e}")
                    

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if sword_sound:
                    sword_sound.play()
                draw_sword_swing()
                if player_rect.colliderect(dragon_rect):
                    dragon_health -= 1
                    player_coins += 10  # Reward for defeating the dragon
                       
                    if dragon_health <= 0:
                        game_phase = GAME_WON  # Change to victory screen instead of resetting

                                            
            if game_phase == CASTLE_TASKS and event.key == pygame.K_u:
                message = upgrade_weapon()
                print(message)
            
    # Move this outside the event loop
    if game_phase == EXPLORE:
        keys = pygame.key.get_pressed()
        old_pos = player_rect.copy()  # Store old position
        is_moving = False      

        if keys[pygame.K_LEFT]:
            player_rect.x -= PLAYER_SPEED
            player_facing_left = True
            is_moving = True
        if keys[pygame.K_RIGHT]:
            player_rect.x += PLAYER_SPEED
            player_facing_left = False
            is_moving = True
        if keys[pygame.K_UP]:
            player_rect.y -= PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_DOWN]:
            player_rect.y += PLAYER_SPEED
            is_moving = True

        # Handle footsteps sound
        current_time = pygame.time.get_ticks()
        if current_time - last_fireball_time > FIREBALL_DELAY:
            shoot_fireball()
            last_fireball_time = current_time
            FIREBALL_DELAY = random.randint(1000, 2000)  # Generate new random delay for next fireball


        if is_moving and footsteps_sound:
            if current_time - footsteps_timer >= FOOTSTEPS_DELAY:
                if footsteps_channel and not footsteps_channel.get_busy():
                    footsteps_channel.play(footsteps_sound)
                    footsteps_timer = current_time
        elif not is_moving and footsteps_channel:
            footsteps_channel.stop()

                # Ograniczenie ruchu do granic ekranu
        player_rect.clamp_ip(screen.get_rect())

    # Game phases
    if game_phase == WELCOME_SCREEN:
        start_rect = draw_welcome_screen()
        
    elif game_phase == EXPLORE:
        screen.blit(background_img, (0, 0))
        draw_player()
        draw_lives()
        
        # Add dragon logic
        move_dragon()
        current_time = pygame.time.get_ticks()
        if current_time - last_fireball_time > FIREBALL_DELAY:
            shoot_fireball()
            last_fireball_time = current_time
        
        update_fireballs()
        draw_dragon_and_fireballs()
        
        # Modified collision check for fireballs
        for fireball in fireballs[:]:
            if player_rect.colliderect(fireball):
                fireballs.remove(fireball)
                player_lives -= 1
                if hit_sound:
                    hit_sound.play()
                # Flash the screen red
                flash_surface = pygame.Surface((WIDTH, HEIGHT))
                flash_surface.fill((255, 0, 0))
                flash_surface.set_alpha(128)
                screen.blit(flash_surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(1000)  # Brief pause to show the flash
                
                if player_lives <= 0:
                    game_phase = GAME_OVER
                else:
                    player_rect.center = (WIDTH // 2, HEIGHT // 2)

    elif game_phase == FIGHT:
        draw_enemies()
        handle_fight()
    elif game_phase == FORTRESS_BOSS:
        draw_enemies()
        fight_boss()
    elif game_phase == CASTLE_TASKS:
        draw_text("W zamku: Naciśnij U, aby ulepszyć broń", 10, 10)
    elif game_phase == GAME_OVER:
        draw_game_over_screen()
    elif game_phase == GAME_WON:
        draw_victory_screen()

    pygame.display.flip()
    clock.tick(30)

# Before pygame.quit()
if footsteps_sound:
    footsteps_sound.stop()
explore_music.stop()
pygame.mixer.quit()
pygame.quit()
sys.exit()