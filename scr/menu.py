from pygame import Rect

class Menu:
    def __init__(self):
        self.buttons = {
            "start": Rect(300, 200, 200, 50),
            "music": Rect(300, 280, 200, 50),
            "quit": Rect(300, 360, 200, 50),
        }

    def draw(self, screen, music_on):
        screen.fill((50, 50, 80))
        screen.draw.text("MAIN MENU", center=(400, 120), fontsize=60, color="white")

        screen.draw.filled_rect(self.buttons["start"], "dodgerblue")
        screen.draw.text("Start Game", center=self.buttons["start"].center, fontsize=40, color="white")

        screen.draw.filled_rect(self.buttons["music"], "seagreen")
        music_text = "Music: ON" if music_on else "Music: OFF"
        screen.draw.text(music_text, center=self.buttons["music"].center, fontsize=40, color="white")

        screen.draw.filled_rect(self.buttons["quit"], "firebrick")
        screen.draw.text("Quit", center=self.buttons["quit"].center, fontsize=40, color="white")

