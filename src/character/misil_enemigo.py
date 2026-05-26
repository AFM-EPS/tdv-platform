import arcade
import math

# Constantes
RIGHT_FACING = 0
LEFT_FACING = 1

# Caché para recursos de la explosión para optimizar el rendimiento
explosion_textures = None
explosion_sound = arcade.load_sound(':resources:sounds/explosion1.wav')


def get_explosion_textures():
    global explosion_textures
    if explosion_textures is None:
        sheet = arcade.load_spritesheet(":resources:images/spritesheets/explosion.png")
        explosion_textures = sheet.get_texture_grid(size=(256, 256), columns=16, count=60)
    return explosion_textures


class Explosion_enemiga(arcade.Sprite):
    """
    Clase que representa una explosión temporal.
    Se auto-reproduce y se destruye al finalizar su animación.
    """

    def __init__(self, x: float, y: float, size: float = 0.5):
        textures = get_explosion_textures()
        super().__init__(textures[0])
        self.textures_list = textures
        self.scale = size
        self.center_x = x
        self.center_y = y
        self.current_frame = 0
        self.time_since_last_frame = 0.0
        self.frame_duration = 0.01  # Duración por frame (rápido y vistoso)
        self.no_collision = True  # Propiedad para que el bucle de colisiones la ignore

        # Reproducir sonido de explosión al crearse
        arcade.play_sound(explosion_sound, volume=0.5)

    def update(self, delta_time: float = 0.016666666666666666, *args, **kwargs):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.frame_duration:
            self.current_frame += 1
            if self.current_frame >= len(self.textures_list):
                self.remove_from_sprite_lists()
            else:
                self.texture = self.textures_list[self.current_frame]
                self.time_since_last_frame = 0.0


class Misil_enemigo(arcade.Sprite):
    """
    Clase que representa un misil enemigo con teleguía de tiempo limitado
    y autodestrucción con explosión.
    """

    def __init__(self, enemigo: arcade.Sprite):
        super().__init__(":resources:images/space_shooter/laserRed01.png", 0.8)
        self.enemigo = enemigo
        self.enmigo = enemigo  # Mantener compatibilidad
        self.jugador = enemigo.jugador
        self.center_x = enemigo.center_x
        self.center_y = enemigo.center_y

        # Velocidad teleguiada (ligeramente más lenta para permitir esquivarlo)
        self.velocidad = enemigo.velocidad_proyectil * 0.5

        # Velocidad de giro en grados por segundo
        self.turn_rate = 100.0

        # Temporizadores de guiado y vida útil
        self.tiempo_guiado = 2  # 2.5 segundos con teleguía activa
        self.tiempo_vida = 2.5  # 3.5 segundos de vida total antes de explotar sola

        # Cálculo de dirección inicial:
        self.angle = 90 - math.degrees(
            math.atan2(enemigo.jugador.center_y - enemigo.center_y, enemigo.jugador.center_x - enemigo.center_x))

    def update(self, delta_time: float = 0.016666666666666666, *args, **kwargs):
        # Descontar tiempo
        self.tiempo_vida -= delta_time
        self.tiempo_guiado -= delta_time

        # Detonación si el tiempo de vida se agota (falló)
        if self.tiempo_vida <= 0:
            self.remove_from_sprite_lists()
            return

        # Guiar sólo si está dentro de su ventana de teleguía activa
        if self.tiempo_guiado > 0 and self.jugador:
            # 1. Calcular ángulo deseado hacia el jugador
            y_diff = self.jugador.center_y - self.center_y
            x_diff = self.jugador.center_x - self.center_x
            desired_angle = 90 - math.degrees(math.atan2(y_diff, x_diff))

            # 2. Calcular la distancia angular más corta (-180 a 180)
            diff = (desired_angle - self.angle + 180) % 360 - 180

            # 3. Limitar la velocidad de rotación según delta_time
            max_turn = self.turn_rate * delta_time
            if abs(diff) <= max_turn:
                self.angle = desired_angle
            else:
                self.angle += math.copysign(max_turn, diff)

        # 4. Actualizar vectores de movimiento basados en el ángulo actual
        theta_rad = math.radians(90 - self.angle)
        self.change_x = self.velocidad * math.cos(theta_rad)
        self.change_y = self.velocidad * math.sin(theta_rad)

        # 5. Llamar al update de la clase padre para aplicar el movimiento físico
        super().update()

    def remove_from_sprite_lists(self):
        if self.sprite_lists:
            # Crear la explosión en la misma posición del misil
            explosion = Explosion_enemiga(self.center_x, self.center_y)
            # Añadir la explosión a todos los SpriteLists en los que estuviese el misil
            for sl in list(self.sprite_lists):
                sl.append(explosion)
        super().remove_from_sprite_lists()
