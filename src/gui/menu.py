import arcade
import arcade.gui
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class MainMenu(arcade.View):

    def __init__(self):
        super().__init__()

        # Manager que controla la interfaz
        self.manager = arcade.gui.UIManager()


        self.background_list = arcade.SpriteList()

        # Fondo sprite
        self.background_sprite = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "background_menu.png")

        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2

        self.background_sprite.width = WINDOW_WIDTH
        self.background_sprite.height = WINDOW_HEIGHT

        self.background_list.append(self.background_sprite)

        # Botones sprites
        self.play_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "play_btn.png")
        self.quit_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "quit_btn.png")
        self.creditos_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "creditos_btn.png")
        self.instrucciones_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "instrucciones_btn.png")
        self.niveles_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "niveles_btn.png")


        # Título textura
        self.title_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "title.png")

        # Sonido
        self.menu_music = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "menu.mp3")
        self.button_press_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "button_press.mp3")
        self.menu_music_player = None

    def on_show_view(self):

        self.manager.enable()
        if self.menu_music_player is None or not self.menu_music_player.playing:
            self.menu_music_player = self.menu_music.play(volume=0.5, loop=True)
            self.window.menu_music_player = self.menu_music_player
            self.window.menu_music = self.menu_music

        # Contenedor vertical
        self.vertical_box = arcade.gui.UIBoxLayout(space_between=20, align="center")
        

        title = arcade.gui.UIImage(texture=self.title_texture, width=650, height=150)
        self.vertical_box.add(title)


        # Botones
        play_btn = arcade.gui.UITextureButton(texture=self.play_btn_sprite, width=256, height=80)
        quit_btn = arcade.gui.UITextureButton(texture=self.quit_btn_sprite, width=256, height=80)
        creditos_btn = arcade.gui.UITextureButton(texture=self.creditos_btn_sprite, width=256, height=80)
        instrucciones_btn = arcade.gui.UITextureButton(texture=self.instrucciones_btn_sprite, width=256, height=80)
        niveles_btn = arcade.gui.UITextureButton(texture=self.niveles_btn_sprite, width=256, height=80)

        # Asociación de eventos de botones
        play_btn.on_click = self.play_game
        quit_btn.on_click = self.exit_game
        creditos_btn.on_click = self.creditos_game
        instrucciones_btn.on_click = self.instrucciones_game
        niveles_btn.on_click = self.niveles_game

        self.vertical_box.add(play_btn)
        self.vertical_box.add(creditos_btn)
        self.vertical_box.add(instrucciones_btn)
        self.vertical_box.add(niveles_btn)
        self.vertical_box.add(quit_btn)


        # Layout para centrar el contenedor
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(
            child=self.vertical_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )


        self.manager.add(anchor_layout)


    def play_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        arcade.play_sound(self.button_press_sound)
        # Detener música del menú
        if self.menu_music_player is not None:
            self.menu_music.stop(self.menu_music_player)
            self.menu_music_player = None
        game_view = GameView()
        self.window.show_view(game_view)

    def creditos_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from gui.creditos import Creditos
        arcade.play_sound(self.button_press_sound)
        game_view = Creditos()
        self.window.show_view(game_view)

    def instrucciones_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from gui.instrucciones import  Instrucciones
        arcade.play_sound(self.button_press_sound)
        game_view = Instrucciones()
        self.window.show_view(game_view)

    def niveles_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from gui.niveles import  Niveles
        arcade.play_sound(self.button_press_sound)
        game_view = Niveles()
        self.window.show_view(game_view)

    def exit_game(self, event):
        arcade.play_sound(self.button_press_sound)
        arcade.exit()

    def on_hide_view(self):
        # Al quitar el menú se desactiva al manager para no perder recursos
        self.manager.disable()

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        self.background_list.draw()

        # Manager dibuja el menú
        self.manager.draw()