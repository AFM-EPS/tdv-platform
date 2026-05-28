from turtle import title

import arcade
import arcade.gui
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class Creditos(arcade.View):

    def __init__(self):
        super().__init__()

        # Manager que controla la interfaz
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        self.background_list = arcade.SpriteList()

        # Fondo sprite
        self.background_sprite = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "background_menu.png")

        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2

        self.background_sprite.width = WINDOW_WIDTH
        self.background_sprite.height = WINDOW_HEIGHT

        self.background_list.append(self.background_sprite)

        # Título textura
        self.title_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "title.png")
        
        self.atras_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "atras_btn.png")

        # Sonido de boton
        self.button_press_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "button_press.mp3")
        
        


    def on_show_view(self):

        self.manager.enable()

        # Contenedor vertical
        self.vertical_box = arcade.gui.UIBoxLayout(space_between=20, align="center")
        

        title = arcade.gui.UIImage(texture=self.title_texture, width=650, height=150)
        self.vertical_box.add(title)

        
        atras_btn = arcade.gui.UITextureButton(texture=self.atras_btn_sprite, width=256, height=80)

        
        atras_btn.on_click = self.atras_game
        #atras_btn.center_x = WINDOW_WIDTH / 2
        #atras_btn.center_y = WINDOW_HEIGHT / 2

        self.vertical_box.add(atras_btn)

        # Layout para centrar el contenedor
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(
            child=self.vertical_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        
        self.manager.add(anchor_layout)
        

        #arcade.draw_lrwh_rectangle_textured(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, self.title_texture)


    def atras_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from gui.menu import MainMenu
        arcade.play_sound(self.button_press_sound)
        game_view = MainMenu()
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        self.background_list.draw()

        # Manager dibuja el menú
        self.manager.draw()
        
        self.credito_0 = arcade.draw_text("Créditos: ", 500, 210,arcade.color.WHITE,24)
        self.credito_1 = arcade.draw_text("Andrew Frassi Machado", 500, 160,arcade.color.WHITE,24)
        self.credito_2 = arcade.draw_text("David Gutiérrez Martínez", 500, 130,arcade.color.WHITE,24)
        self.credito_3 = arcade.draw_text("Marcos Serrano Fernández", 500, 100,arcade.color.WHITE,24)
        self.credito_4 = arcade.draw_text("Alberto Cerezo Jiménez", 500, 70,arcade.color.WHITE,24)
        