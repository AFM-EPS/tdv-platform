import arcade
import math
#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1

#Velocidad!
VELOCIDAD = 12

class Proyectil(arcade.Sprite):
    """
        DOCSTRING
        La clase es un proyectil
        La orientación debe estar en radianes

    """
    def __init__(self, jugador,orientation:float=0):
        super().__init__(":resources:images/space_shooter/laserBlue01.png",0.8)
        self.jugador = jugador
        self.center_x = jugador.arma.center_x
        self.center_y = jugador.arma.center_y
        #Cálculo de dirección:
        self.change_x = math.cos(orientation) * VELOCIDAD
        self.change_y = math.sin(orientation) * VELOCIDAD

        self.angle = 360 - math.degrees(orientation)

