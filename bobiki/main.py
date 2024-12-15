import pygame
import random
import sys
import os

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (105, 105, 105)
WELCOME_SCREEN = "welcome"
EXPLORE = "explore"
FIGHT = "fight"
FORTRESS_BOSS = "fortress_boss"
CASTLE_TASKS = "castle_tasks"
GAME_OVER = "game_over"
GAME_WON = "game_won"
PLAYER_SPEED = 5
FIREBALL_SPEED = 10

# Initialize Pygame
pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)

class SoundManager:
    def __init__(self):
        self.explore_music = self.load_sound("music/explore.wav", 0.1)
        self.footsteps_sound = self.load_sound("music/player/footsteps.mp3", 0.6)
        self.hit_sound = self.load_sound("music/hit.wav", 0.3)
        self.sword_sound = self.load_sound("music/sword.wav", 0.4)
        self.footsteps_channel = pygame.mixer.Channel(1) if self.footsteps_sound else None

    def load_sound(self, path, volume):
        try:
            sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, path))
            sound.set_volume(volume)
            return sound
        except pygame.error as e:
            print(f"Couldn't load sound {path}: {e}")
            return None

    def play_sound(self, sound):
        if sound:
            sound.play()

    def stop_sound(self, sound):
        if sound:
            sound.stop()

class Player:
    def __init__(self, image):
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.health = 20
        self.damage = 5
        self.lives = 3
        self.facing_left = False
        self.is_moving = False
        self.footsteps_timer = 0

    def draw(self, screen):
        if self.facing_left:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            screen.blit(self.image, self.rect)

    def move(self, keys):
        old_pos = self.rect.copy()
        self.is_moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.facing_left = True
            self.is_moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.facing_left = False
            self.is_moving = True
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            self.is_moving = True

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

class Dragon:
    def __init__(self, image, heart_image):
        self.image = pygame.transform.scale(image, (200, 200))
        self.rect = self.image.get_rect(x=WIDTH - 200, y=100)
        self.speed = 3
        self.direction = 1
        self.health = 5
        self.heart_image = pygame.transform.scale(heart_image, (30, 30))
        self.fireballs = []
        self.last_fireball_time = 0
        self.fireball_delay = random.randint(800, 2200)

    def move(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.direction *= -1

    def shoot_fireball(self):
        fireball = pygame.Rect(self.rect.left, self.rect.centery, 30, 30)
        self.fireballs.append(fireball)

    def update_fireballs(self):
        for fireball in self.fireballs[:]:
            fireball.x -= FIREBALL_SPEED
            if fireball.right < 0:
                self.fireballs.remove(fireball)

    def draw(self, screen, fireball_img):
        screen.blit(self.image, self.rect)
        for fireball in self.fireballs:
            screen.blit(fireball_img, fireball)

    def draw_hearts(self, screen):
        heart_spacing = 35
        start_x = WIDTH - (heart_spacing * self.health) - 10
        start_y = 10
        for i in range(self.health):
            screen.blit(self.heart_image, (start_x + (i * heart_spacing), start_y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bobiki: Zamek i Fortece")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 74)
        self.background_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "images/background.png")), (WIDTH, HEIGHT))
        self.castle_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/castle.png"))
        self.fortress_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/fortress.png"))
        self.zombie_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/zombie.png"))
        self.orc_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/orc.png"))
        self.boss_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/boss.png"))
        self.coin_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/coin.png"))
        self.sword_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/sword.png"))
        
        self.heart_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/heart.png"))
        self.heart_img = pygame.transform.scale(self.heart_img, (30, 30))

        self.dragon_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/dragon.png"))
        
        self.fireball_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/fireball.png"))
        self.fireball_img = pygame.transform.scale(self.fireball_img, (30, 30))

        self.dragon_heart_img = pygame.image.load(os.path.join(ASSETS_DIR, "images/dragon-heart.png"))
        self.sound_manager = SoundManager()
        self.player = Player(pygame.image.load(os.path.join(ASSETS_DIR, "images/player3.png")))
        self.dragon = Dragon(self.dragon_img, self.dragon_heart_img)
        self.enemies = [
            {"type": "zombie", "health": 10, "damage": 3, "position": (250, 350)},
            {"type": "orc", "health": 20, "damage": 5, "position": (500, 450)},
        ]
        self.boss = {"type": "mag", "health": 50, "damage": 10, "position": (WIDTH // 2 - 50, 100)}
        self.game_phase = WELCOME_SCREEN

    def draw_text(self, text, x, y, color=WHITE):
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))

    def draw_castle(self):
        self.screen.blit(self.castle_img, (WIDTH // 2 - 100, HEIGHT // 2 - 200))
        self.draw_text("Zamek: Kliknij, aby wejść", WIDTH // 2 - 100, HEIGHT // 2 - 230)

    def draw_fortresses(self):
        for pos in [(200, 300), (400, 400), (600, 200)]:
            self.screen.blit(self.fortress_img, pos)
        self.draw_text("Fortece: Kliknij, aby walczyć", 10, 10)

    def draw_enemies(self):
        for enemy in self.enemies:
            if enemy["type"] == "zombie":
                self.screen.blit(self.zombie_img, enemy["position"])
            elif enemy["type"] == "orc":
                self.screen.blit(self.orc_img, enemy["position"])
        if self.game_phase == "fortress_boss":
            self.screen.blit(self.boss_img, self.boss["position"])

    def handle_fight(self):
        for enemy in self.enemies:
            if random.random() < 0.5:
                self.player.health -= enemy["damage"]
            enemy["health"] -= self.player.damage
            if enemy["health"] <= 0:
                self.enemies.remove(enemy)
        if self.player.health <= 0:
            self.player.lives -= 1
            
            if self.player.lives <= 0:
                self.game_phase = GAME_OVER
            else:
                self.player.health = 20
        if not self.enemies:
            self.game_phase = "fortress_boss"

    def fight_boss(self):
        self.player.health -= self.boss["damage"]
        self.boss["health"] -= self.player.damage
        if self.boss["health"] <= 0:
            self.draw_text("Pokonałeś bossa! Gratulacje!", WIDTH // 2 - 100, HEIGHT // 2 - 50)
            self.game_phase = "explore"

    def upgrade_weapon(self):
        pass

    def draw_welcome_screen(self):
        self.screen.blit(pygame.transform.scale(self.castle_img, (WIDTH, HEIGHT)), (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        title_text = self.title_font.render("Bobik walczy ze smokiem", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        self.screen.blit(title_text, title_rect)
        start_text = self.font.render("Kliknij, aby rozpocząć grę", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
        self.screen.blit(start_text, start_rect)
        return start_rect

    def draw_game_over_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(192)
        self.screen.blit(overlay, (0, 0))
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        self.screen.blit(game_over_text, game_over_rect)
        restart_text = self.font.render("Click to Play Again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
        self.screen.blit(restart_text, restart_rect)
        return restart_rect

    def draw_victory_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(192)
        self.screen.blit(overlay, (0, 0))
        victory_text = self.title_font.render("YOU WON!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        self.screen.blit(victory_text, victory_rect)
        restart_text = self.font.render("Click to Play Again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
        self.screen.blit(restart_text, restart_rect)
        return restart_rect

    def reset_game(self):
        self.player.health = 20
        self.player.damage = 5
        self.player.lives = 3
        self.dragon.health = 5
        self.player.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.enemies = [
            {"type": "zombie", "health": 10, "damage": 3, "position": (250, 350)},
            {"type": "orc", "health": 20, "damage": 5, "position": (500, 450)},
        ]
        self.boss = {"type": "mag", "health": 50, "damage": 10, "position": (WIDTH // 2 - 50, 100)}
        self.dragon.fireballs.clear()
        self.game_phase = EXPLORE
        self.sound_manager.stop_sound(self.sound_manager.explore_music)
        self.sound_manager.play_sound(self.sound_manager.explore_music)

    def draw_player_lives(self):
        heart_spacing = 35
        start_x = 10
        start_y = 10
        for i in range(self.player.lives):
            self.screen.blit(self.heart_img, (start_x + (i * heart_spacing), start_y))

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.game_phase == WELCOME_SCREEN:
                        start_rect = self.draw_welcome_screen()
                        if start_rect.collidepoint(x, y):
                            self.game_phase = EXPLORE
                            self.sound_manager.play_sound(self.sound_manager.explore_music)
                    if self.game_phase == GAME_OVER:
                        restart_rect = self.draw_game_over_screen()
                        if restart_rect.collidepoint(x, y):
                            self.reset_game()
                    if self.game_phase == GAME_WON:
                        restart_rect = self.draw_victory_screen()
                        if restart_rect.collidepoint(x, y):
                            self.reset_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.sound_manager.play_sound(self.sound_manager.sword_sound)
                        if self.player.rect.colliderect(self.dragon.rect):
                            self.dragon.health -= 1
                            if self.dragon.health <= 0:
                                self.game_phase = GAME_WON
                    if self.game_phase == CASTLE_TASKS and event.key == pygame.K_u:
                        message = self.upgrade_weapon()
                        print(message)

            if self.game_phase == EXPLORE:
                keys = pygame.key.get_pressed()
                self.player.move(keys)
                current_time = pygame.time.get_ticks()
                if current_time - self.dragon.last_fireball_time > self.dragon.fireball_delay:
                    self.dragon.shoot_fireball()
                    self.dragon.last_fireball_time = current_time
                    self.dragon.fireball_delay = random.randint(1000, 2000)
                if self.player.is_moving and self.sound_manager.footsteps_sound:
                    if current_time - self.player.footsteps_timer >= 300:
                        if self.sound_manager.footsteps_channel and not self.sound_manager.footsteps_channel.get_busy():
                            self.sound_manager.footsteps_channel.play(self.sound_manager.footsteps_sound)
                            self.player.footsteps_timer = current_time
                elif not self.player.is_moving and self.sound_manager.footsteps_channel:
                    self.sound_manager.footsteps_channel.stop()
                self.draw_player_lives()

            if self.game_phase == WELCOME_SCREEN:
                self.draw_welcome_screen()
            elif self.game_phase == EXPLORE:
                self.screen.blit(self.background_img, (0, 0))
                self.player.draw(self.screen)
                self.dragon.move()
                self.dragon.update_fireballs()
                self.dragon.draw(self.screen, self.fireball_img)
                self.dragon.draw_hearts(self.screen)
                self.draw_player_lives()
                for fireball in self.dragon.fireballs[:]:
                    if self.player.rect.colliderect(fireball):
                        self.dragon.fireballs.remove(fireball)
                        self.player.lives -= 1
                        self.player.rect.center = PLAYER_START_POSITION
                        self.sound_manager.play_sound(self.sound_manager.hit_sound)
                        flash_surface = pygame.Surface((WIDTH, HEIGHT))
                        flash_surface.fill((255, 0, 0))
                        flash_surface.set_alpha(128)
                        self.screen.blit(flash_surface, (0, 0))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        if self.player.lives <= 0:
                            self.game_phase = GAME_OVER
                        else:
                            self.player.rect.center = (WIDTH // 2, HEIGHT // 2)
            elif self.game_phase == FIGHT:
                self.draw_enemies()
                self.handle_fight()
                self.draw_player_lives()
            elif self.game_phase == FORTRESS_BOSS:
                self.draw_enemies()
                self.fight_boss()
                self.draw_player_lives()
            elif self.game_phase == CASTLE_TASKS:
                self.draw_text("W zamku: Naciśnij U, aby ulepszyć broń", 10, 10)
            elif self.game_phase == GAME_OVER:
                self.draw_game_over_screen()
            elif self.game_phase == GAME_WON:
                self.draw_victory_screen()

            pygame.display.flip()
            self.clock.tick(30)

        self.sound_manager.stop_sound(self.sound_manager.footsteps_sound)
        self.sound_manager.stop_sound(self.sound_manager.explore_music)
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()