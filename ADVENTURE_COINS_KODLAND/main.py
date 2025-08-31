# platformer_compact.py
import random
import math
from pygame import Rect

# Configurações
TITLE, WIDTH, HEIGHT = "ADVENTURE COINS", 800, 600
BLUE, RED, GREEN, YELLOW = (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)
BROWN, SKY_BLUE, BLACK, WHITE = (139, 69, 19), (135, 206, 235), (0, 0, 0), (255, 255, 255)
PURPLE, LIGHT_GREEN, LIGHT_RED = (128, 0, 128), (144, 238, 144), (255, 99, 71)
MENU, PLAYING, GAME_OVER = 0, 1, 2

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action=None):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, color=BLACK, fontsize=28)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()
            return True
        return False

class GameObject:
    def __init__(self, x, y, w, h, color=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        screen.draw.filled_rect(self.get_rect(), self.color)

class Hero(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60, BLUE)
        self.velocity_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.is_jumping = False
    
    def update(self, platforms):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        hero_rect = self.get_rect()
        for p in platforms:
            if hero_rect.colliderect(p.get_rect()):
                if self.velocity_y > 0: 
                    self.y = p.y - self.height
                    self.velocity_y = 0
                    self.is_jumping = False
                elif self.velocity_y < 0: 
                    self.y = p.y + p.height
                    self.velocity_y = 0
        
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.is_jumping = False
    
    def move(self, direction):
        self.x = max(0, min(WIDTH - self.width, self.x + direction * 5))
    
    def jump(self):
        if not self.is_jumping: 
            self.velocity_y = self.jump_power
            self.is_jumping = True
    
    def draw(self, screen):
        super().draw(screen)
        eye_y = self.y + 15
        screen.draw.filled_circle((self.x + 15, eye_y), 5, WHITE)
        screen.draw.filled_circle((self.x + 25, eye_y), 5, WHITE)

class Enemy(GameObject):
    def __init__(self, x, y, max_dist=100):
        super().__init__(x, y, 30, 30, PURPLE)
        self.direction = 1
        self.distance = 0
        self.max_distance = max_dist
    
    def update(self):
        self.x += self.direction * 2
        self.distance += abs(self.direction * 2)
        if self.distance >= self.max_distance: 
            self.direction *= -1
            self.distance = 0
    
    def draw(self, screen):
        super().draw(screen)
        screen.draw.filled_circle((self.x + 10, self.y + 10), 4, WHITE)
        screen.draw.filled_circle((self.x + 20, self.y + 10), 4, WHITE)
        screen.draw.line((self.x + 8, self.y + 22), (self.x + 22, self.y + 22), BLACK)

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, YELLOW)
        self.collected = False
    
    def draw(self, screen, frame_count):
        if not self.collected:
            size = self.width * (math.sin(frame_count * 0.1) * 0.2 + 0.8)
            screen.draw.filled_circle((self.x + self.width//2, self.y + self.height//2), size/2, YELLOW)
            screen.draw.filled_circle((self.x + self.width//3, self.y + self.height//3), 4, (255, 255, 200))

class Game:
    def __init__(self):
        self.state = MENU
        self.score = 0
        self.frame_count = 0
        self.sound_enabled = True
        self.setup_menu()
        self.init_game()
        self.play_background_music()
    
    def setup_menu(self):
        x = WIDTH // 2 - 100
        self.menu_buttons = [
            Button(x, 250, 200, 50, "Começar Jogo", GREEN, LIGHT_GREEN, self.start_game),
            Button(x, 320, 200, 50, "Som: ON", YELLOW, (255, 255, 150), self.toggle_sound),
            Button(x, 390, 200, 50, "Sair", RED, LIGHT_RED, self.quit_game)
        ]
    
    def init_game(self):
        self.score = 0
        self.hero = Hero(100, HEIGHT - 110)
        self.platforms = [
            GameObject(0, HEIGHT-40, WIDTH, 40, BROWN),
            GameObject(100, 450, 200, 20, BROWN),
            GameObject(400, 400, 150, 20, BROWN),
            GameObject(200, 350, 100, 20, BROWN),
            GameObject(500, 300, 200, 20, BROWN),
            GameObject(100, 250, 150, 20, BROWN),
            GameObject(350, 200, 100, 20, BROWN),
            GameObject(600, 150, 150, 20, BROWN)
        ]
        self.enemies = [Enemy(300, HEIGHT-70), Enemy(550, 370), Enemy(150, 230)]
        self.coins = [Coin(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-100)) for _ in range(10)]
    
    def play_background_music(self):
        if self.sound_enabled and hasattr(music, 'play'):
            try:
                music.play('background_music')
                music.set_volume(0.5)
            except:
                print("Erro ao reproduzir música de fundo")
    
    def stop_background_music(self):
        if hasattr(music, 'stop'):
            music.stop()
    
    def start_game(self):
        self.state = PLAYING
        self.init_game()
        self.play_background_music()
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        for b in self.menu_buttons:
            if b.text.startswith("Som:"):
                b.text = f"Som: {'ON' if self.sound_enabled else 'OFF'}"
                break
        
        if self.sound_enabled:
            self.play_background_music()
        else:
            self.stop_background_music()
    
    def quit_game(self):
        exit()

    def update(self):
        self.frame_count += 1
        if self.state == PLAYING:
            if keyboard.left:
                self.hero.move(-1)
            if keyboard.right:
                self.hero.move(1)
            
            self.hero.update(self.platforms)
            
            for e in self.enemies:
                e.update()
                if self.hero.get_rect().colliderect(e.get_rect()):
                    self.state = GAME_OVER
                    if self.sound_enabled and hasattr(sounds, 'death'):
                        sounds.death.play()
            
            for c in self.coins:
                if not c.collected and self.hero.get_rect().colliderect(c.get_rect()):
                    c.collected = True
                    self.score += 10
                    if self.sound_enabled and hasattr(sounds, 'coin'):
                        sounds.coin.play()
            
            if all(c.collected for c in self.coins):
                for c in self.coins:
                    c.x = random.randint(50, WIDTH-50)
                    c.y = random.randint(50, HEIGHT-100)
                    c.collected = False

    def draw(self, screen):
        screen.clear()
        screen.fill(SKY_BLUE)
        
        for i in range(3):
            cloud_x = (self.frame_count * 2 + i * 300) % (WIDTH + 300) - 150
            screen.draw.filled_circle((cloud_x, 50+i*60), 25, WHITE)
            screen.draw.filled_circle((cloud_x+25, 35+i*60), 20, WHITE)
            screen.draw.filled_circle((cloud_x+50, 60+i*60), 20, WHITE)
        
        if self.state == MENU:
            screen.draw.text("ADVENTURE COINS", (WIDTH//2-150, 100), color=BLACK, fontsize=48)
            screen.draw.text("Use SETAS para mover e ESPAÇO para pular", (WIDTH//2-170, 150), color=BLACK, fontsize=26)
            for b in self.menu_buttons:
                b.draw(screen)
        elif self.state == PLAYING:
            for p in self.platforms:
                p.draw(screen)
            for e in self.enemies:
                e.draw(screen)
            for c in self.coins:
                c.draw(screen, self.frame_count)
            self.hero.draw(screen)
            screen.draw.text(f"Pontos: {self.score}", (10, 10), color=BLACK, fontsize=36)
        elif self.state == GAME_OVER:
            screen.draw.text("GAME OVER", (WIDTH//2-150, 100), color=RED, fontsize=72)
            screen.draw.text(f"Pontuação Final: {self.score}", (WIDTH//2-110, 150), color=BLACK, fontsize=36)
            screen.draw.text("Pressione ESPAÇO para jogar novamente", (WIDTH//2-160, 250), color=BLACK, fontsize=24)
    
    def on_key_down(self, key):
        if key == keys.SPACE:
            if self.state in [MENU, GAME_OVER]:
                self.start_game()
            elif self.state == PLAYING:
                self.hero.jump()
                if self.sound_enabled and hasattr(sounds, 'jump'):
                    sounds.jump.play()
        
    
    def on_mouse_move(self, pos):
        if self.state == MENU:
            for b in self.menu_buttons:
                b.check_hover(pos)
    
    def on_mouse_down(self, pos):
        if self.state == MENU:
            for b in self.menu_buttons:
                if b.check_click(pos):
                    break

# Instância global do jogo
game = Game()

# Funções do Pygame Zero
def update():
    game.update()

def draw():
    game.draw(screen)

def on_key_down(key):
    game.on_key_down(key)

def on_mouse_move(pos):
    game.on_mouse_move(pos)

def on_mouse_down(pos):
    game.on_mouse_down(pos)
