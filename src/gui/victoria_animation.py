import arcade
from pathlib import Path

# Librería para mostrar vídeos (OpenCV)
import cv2
# Uso PIL para convertir datos de OpenCV a texturas que Arcade pueda interpretar
from PIL import Image


PROJECT_ROOT = Path(__file__).parent.parent.parent

class Victoria_Animation(arcade.View):

    def __init__(self, next_view):

        super().__init__()

        # View que se cargará tras la animación
        self.next_view = next_view
        
        # Cargar el vídeo
        self.video = cv2.VideoCapture(PROJECT_ROOT / "assets" / "videos" / "VIDEO_PROVISIONAL_VICTORIA.mp4")

        # Cargar audio del vídeo
        audio_path = PROJECT_ROOT / "assets" / "music" / "animation-alpha-audio.mp3"
        self.video_sound = arcade.load_sound(audio_path)
        self.sound_player = None
        
        # Sprite y spriteList para envolver el vídeo
        self.sprite = arcade.Sprite()
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.sprite)

        # Indicador de que el vídeo ha comenzado
        self.video_started = False

        self.instructions_list = []

        titulo = arcade.Text("¡Victoria!", self.window.width / 2, self.window.height / 2, arcade.color.WHITE, 48, anchor_x="center", font_name="Impact")
        self.instructions_list.append(titulo)

        text = arcade.Text("Click para continuar", self.window.width / 2, self.window.height / 2 - (40*2), arcade.color.WHITE, 24, anchor_x="center", font_name="Impact")
        self.instructions_list.append(text)


    def on_show_view(self):

        # Ajustar sprite al centro de la pantalla
        self.sprite.center_x = self.window.width / 2
        self.sprite.center_y = self.window.height / 2


        # Reproducir sonido
        self.sound_player = arcade.play_sound(self.video_sound)


    def on_update(self, delta_time):

        # La función read() devuelve una tupla:
        # El primer elemento es un booleano e indica si la lectura fue exitosa (True) o si se terminó (False) (cosa que guardo en ret)
        # El segundo elemento es la matriz de píxeles del vídeo (es decir, un array, que es lo que devuelve OpenCV) (cosa que guardo en frame)
        ret, frame = self.video.read()
        
        # Si el vídeo se termina
        if not ret: 
            self.video.release()

            # Detener audio
            if self.sound_player:
                arcade.stop_sound(self.sound_player)

            # Mostrar siguiente vista
            self.window.show_view(self.next_view)

            return
        
        # Se crea un frame en el que se ajusta la resolución del vídeo a la pantalla del juego (machaco el frame original sin el resize para ahorrar sus recursos)
        frame = cv2.resize(frame, (self.window.width, self.window.height))
            
        # Función para convertir el color del frame de BGR (que es lo que usa OpenCV) a RGBA (que es lo que usa Arcade)
        frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        # Transformar matriz de píxeles a objeto Image que Arcade puede interpretar
        image = Image.fromarray(frame_rgba)
        
        # Se establece la textura del vídeo en el sprite
        self.sprite.texture = arcade.Texture(image)

        # Se ajustan las dimensiones del sprite a las de la pantalla
        self.sprite.width = self.window.width
        self.sprite.height = self.window.height

        # Indicar que ya hay un fotograma válido y que se puede empezar a dibujar (ya que si no puede haber glitches morados y negros al inicio)
        self.video_started = True


    def on_draw(self):
        self.clear()
        
        # Si hay fotograma válido, se dibuja el sprite list
        if self.video_started:
            self.sprite_list.draw()

        # Dibujar instrucciones
        for line in self.instructions_list:
            line.draw()


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.video.release()

        if self.sound_player:
            arcade.stop_sound(self.sound_player)
            
        self.window.show_view(self.next_view)