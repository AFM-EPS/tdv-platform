import arcade
from pathlib import Path
from gui.menu import MainMenu


PROJECT_ROOT = Path(__file__).parent.parent.parent
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class VictoryView(arcade.View):

    def __init__(self):
        super().__init__()


        self.background_list = arcade.SpriteList()

        # Fondo sprite
        self.background_sprite = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "victory.png")

        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2

        self.background_sprite.width = WINDOW_WIDTH
        self.background_sprite.height = WINDOW_HEIGHT

        self.background_list.append(self.background_sprite)


    def on_mouse_press(self, _x, _y, _button, _modifiers):

        self.window.show_view(MainMenu())


    def on_draw(self):
        self.clear()

        # Dibujar fondo
        self.background_list.draw()