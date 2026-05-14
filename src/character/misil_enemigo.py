import arcade
import math
#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1

#Velocidad!
class Misil_enemigo(arcade.Sprite):
    """
        DOCSTRING
        La clase es un proyectil
        La orientación debe estar en radianes

    """
    def __init__(self,enemigo:arcade.Sprite):
        super().__init__(":resources:images/space_shooter/laserRed01.png",0.8)
        self.enmigo = enemigo
        self.jugador = enemigo.jugador
        self.center_x = enemigo.center_x
        self.center_y = enemigo.center_y

        self.velocidad = 0
        #Cálculo de dirección:
        self.angle = 90 - math.degrees(math.atan2(enemigo.jugador.center_y - enemigo.center_y, enemigo.jugador.center_x - enemigo.center_x))

