import arcade
from pathlib import Path

# Librería para mostrar vídeos (OpenCV)
import cv2
# Uso PIL para convertir datos de OpenCV a texturas que Arcade pueda interpretar
from PIL import Image



class Animation(arcade.View):

    def __init__(self, next_view, video_path, audio_path):

        super().__init__()

        # View que se cargará tras la animación
        self.next_view = next_view
        
        # Cargar el vídeo
        self.video = cv2.VideoCapture(video_path)

        # Cargar audio del vídeo
        self.video_sound = arcade.load_sound(audio_path)
        self.sound_player = None
        
        # Sprite y spriteList para envolver el vídeo
        self.sprite = arcade.Sprite()
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.sprite)

        # Indicador de que el vídeo ha comenzado
        self.video_started = False


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


    def on_key_press(self, key, modifiers):

        # Saltar animación
        if key == arcade.key.ESCAPE:
            self.video.release()

            if self.sound_player:
                arcade.stop_sound(self.sound_player)
            
            self.window.show_view(self.next_view)