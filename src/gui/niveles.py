import arcade
import arcade.gui
import persistence
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class Niveles(arcade.View):

    def __init__(self):
        super().__init__()

        # Manager que controla la interfaz
        self.manager = arcade.gui.UIManager()

        self.unlocked_levels = [1]
        self.high_score = 0
        self.level_buttons = {}


        self.background_list = arcade.SpriteList()

        # Fondo sprite
        self.background_sprite = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "background_menu.png")

        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2

        self.background_sprite.width = WINDOW_WIDTH
        self.background_sprite.height = WINDOW_HEIGHT

        self.background_list.append(self.background_sprite)

        # Botones sprites
        
        self.atras_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "back_btn.png")
        self.nivel_1_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "level_1_btn.png")
        self.nivel_2_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "level_2_btn.png")
        self.nivel_3_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "level_3_btn.png")
        self.nivel_4_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "level_4_btn.png")
        self.nivel_final_btn_sprite = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "final_level_btn.png")
        # Título textura
        self.title_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "title.png")

        # Sonido de boton
        self.button_press_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "button_press.mp3")

        # Texto score máximo
        self.max_score_text = arcade.Text(
            f"PUNTUACIÓN MÁXIMA: {self.high_score}",
            WINDOW_WIDTH / 2,
            40,
            arcade.color.GOLDEN_YELLOW,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name="Impact"
        )

    def on_show_view(self):

        self.manager.enable()

        # Recargar datos de persistencia actualizados
        self.unlocked_levels = persistence.get_unlocked_levels()
        self.high_score = persistence.get_high_score()


        # Contenedor vertical
        self.vertical_box = arcade.gui.UIBoxLayout(space_between=20, align="center")
        

        title = arcade.gui.UIImage(texture=self.title_texture, width=650, height=150)
        self.vertical_box.add(title)


        # Botones
        atras_btn = arcade.gui.UITextureButton(texture=self.atras_btn_sprite, width=192, height=64)
        nivel_1_btn = arcade.gui.UITextureButton(texture=self.nivel_1_btn_sprite, width=192, height=64)
        nivel_2_btn = arcade.gui.UITextureButton(texture=self.nivel_2_btn_sprite, width=192, height=64)
        nivel_3_btn = arcade.gui.UITextureButton(texture=self.nivel_3_btn_sprite, width=192, height=64)
        nivel_4_btn = arcade.gui.UITextureButton(texture=self.nivel_4_btn_sprite, width=192, height=64)
        nivel_final_btn = arcade.gui.UITextureButton(texture=self.nivel_final_btn_sprite, width=192, height=64)

        # Registrar botones para control de bloqueados
        self.level_buttons = {
            1: nivel_1_btn,
            2: nivel_2_btn,
            3: nivel_3_btn,
            4: nivel_4_btn,
            5: nivel_final_btn
        }

        # Asociación de eventos de botones
        atras_btn.on_click = self.atras_game
        nivel_1_btn.on_click = self.nivel_1_game
        nivel_2_btn.on_click = self.nivel_2_game
        nivel_3_btn.on_click = self.nivel_3_game
        nivel_4_btn.on_click = self.nivel_4_game
        nivel_final_btn.on_click = self.nivel_final_game


        self.vertical_box.add(nivel_1_btn)
        self.vertical_box.add(nivel_2_btn)
        self.vertical_box.add(nivel_3_btn)
        self.vertical_box.add(nivel_4_btn)
        self.vertical_box.add(nivel_final_btn)
        self.vertical_box.add(atras_btn)


        # Layout para centrar el contenedor
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(
            child=self.vertical_box,
            anchor_x="center_x",
            anchor_y="top"
        )


        self.manager.add(anchor_layout)

    def atras_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from gui.menu import MainMenu
        game_view = MainMenu()
        arcade.play_sound(self.button_press_sound)
        self.window.show_view(game_view)

    def play_game(self, event):
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        game_view = GameView()
        arcade.play_sound(self.button_press_sound)
        self.window.show_view(game_view)

    def nivel_1_game(self, event):
        if 1 not in self.unlocked_levels:
            return
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        arcade.play_sound(self.button_press_sound)

        # Detener música del menú
        if hasattr(self.window, 'menu_music_player') and self.window.menu_music_player:
            self.window.menu_music.stop(self.window.menu_music_player)
            self.window.menu_music_player = None

        game_view = GameView()
        game_view.map_num = 1
        game_view.setup()
        self.window.show_view(game_view)

    def nivel_2_game(self, event):
        if 2 not in self.unlocked_levels:
            return
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        arcade.play_sound(self.button_press_sound)

        # Detener música del menú
        if hasattr(self.window, 'menu_music_player') and self.window.menu_music_player:
            self.window.menu_music.stop(self.window.menu_music_player)
            self.window.menu_music_player = None

        game_view = GameView()
        game_view.map_num = 2
        game_view.setup()
        self.window.show_view(game_view)

    def nivel_3_game(self, event):
        if 3 not in self.unlocked_levels:
            return
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        arcade.play_sound(self.button_press_sound)

        # Detener música del menú
        if hasattr(self.window, 'menu_music_player') and self.window.menu_music_player:
            self.window.menu_music.stop(self.window.menu_music_player)
            self.window.menu_music_player = None

        game_view = GameView()
        game_view.map_num = 3
        game_view.setup()
        self.window.show_view(game_view)

    def nivel_4_game(self, event):
        if 4 not in self.unlocked_levels:
            return
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        arcade.play_sound(self.button_press_sound)

        # Detener música del menú
        if hasattr(self.window, 'menu_music_player') and self.window.menu_music_player:
            self.window.menu_music.stop(self.window.menu_music_player)
            self.window.menu_music_player = None
            
        game_view = GameView()
        game_view.map_num = 4
        game_view.setup()
        self.window.show_view(game_view)

    def nivel_final_game(self, event):
        if 5 not in self.unlocked_levels:
            return
        # Se hace el import aquí para evitar error por bucle infinito de import circular
        from main import GameView
        arcade.play_sound(self.button_press_sound)
        # Detener música del menú
        if hasattr(self.window, 'menu_music_player') and self.window.menu_music_player:
            self.window.menu_music.stop(self.window.menu_music_player)
            self.window.menu_music_player = None
        game_view = GameView()
        game_view.map_num = 5
        game_view.setup()
        self.window.show_view(game_view)

    def on_hide_view(self):
        # Al quitar el menú se desactiva al manager para no perder recursos
        self.manager.disable()

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        self.background_list.draw()

        # Manager dibuja el menú
        self.manager.draw()

        # Dibujar indicador de puntuación récord (High Score)
        self.max_score_text.draw()

        # Dibujar capa de bloqueo sobre los niveles que no están desbloqueados
        for level_num, btn in self.level_buttons.items():
            if level_num not in self.unlocked_levels:
                # Dibujar rectángulo translúcido gris oscuro
                arcade.draw_lbwh_rectangle_filled(
                    btn.left,
                    btn.bottom,
                    btn.width,
                    btn.height,
                    (30, 30, 30, 200)  # Gris oscuro translúcido
                )
                # Dibujar texto de bloqueo elegante
                arcade.Text(
                    "🔒 BLOQUEADO",
                    btn.left + btn.width / 2,
                    btn.bottom + btn.height / 2,
                    arcade.color.LIGHT_GRAY,
                    font_size=12,
                    anchor_x="center",
                    anchor_y="center",
                    font_name="Impact",
                    bold=True
                ).draw()