import pgzrun
from hero import Hero
from enemy import Enemy
from menu import Menu

# Window
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Test Game"

# States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
game_state = STATE_MENU

# Music
music_on = True

# Entities
hero = Hero((400, 500))
enemies = [
    Enemy((200, 500), 150, 300),
    Enemy((600, 500), 550, 750)
]

# Menu
menu = Menu()

# ---------------- DRAW -----------------
def draw():
    if game_state == STATE_MENU:
        menu.draw(screen, music_on)
    elif game_state == STATE_PLAYING:
        screen.fill((100, 180, 240))
        hero.draw()
        for enemy in enemies:
            enemy.draw()
    elif game_state == STATE_GAME_OVER:
        screen.fill((30, 0, 0))
        screen.draw.text("GAME OVER", center=(400, 300), fontsize=80, color="red")
        screen.draw.text("Click to return", center=(400, 400), fontsize=40, color="white")

# ---------------- UPDATE -----------------
def update():
    global game_state
    if game_state == STATE_PLAYING:
        hero.update(keyboard)
        for enemy in enemies:
            enemy.update()
            if hero.rect.colliderect(enemy.rect):
                sounds.hit.play()
                game_state = STATE_GAME_OVER

# ---------------- INPUT -----------------
def on_mouse_down(pos):
    global game_state, music_on
    if game_state == STATE_MENU:
        if menu.buttons["start"].collidepoint(pos):
            game_state = STATE_PLAYING
            if music_on:
                music.play("bg_music")
        elif menu.buttons["music"].collidepoint(pos):
            music_on = not music_on
            if not music_on:
                music.stop()
        elif menu.buttons["quit"].collidepoint(pos):
            exit()
    elif game_state == STATE_GAME_OVER:
        game_state = STATE_MENU

pgzrun.go()

