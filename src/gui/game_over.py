import arcade
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class GameOverView(arcade.View):

    def __init__(self, map_num):
        super().__init__()

        # Guardar mapa en el que el jugador murió
        self.map_num = map_num


        self.background_list = arcade.SpriteList()

        # Fondo sprite
        self.background_sprite = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "game_over.png")

        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2

        self.background_sprite.width = WINDOW_WIDTH
        self.background_sprite.height = WINDOW_HEIGHT

        self.background_list.append(self.background_sprite)


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView

        game_view = GameView()
        game_view.map_num = self.map_num
        self.window.show_view(game_view)


    def on_draw(self):
        self.clear()

        # Dibujar fondo
        self.background_list.draw()