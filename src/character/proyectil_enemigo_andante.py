import arcade
import math
#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1
#OFFSETS
OFFSET_X = -5
OFFSET_Y = 35

#Velocidad!
class Proyectil_enemigo_andante(arcade.Sprite):
    """
        DOCSTRING
        La clase es un proyectil
        La orientación debe estar en radianes

    """
    def __init__(self,enemigo,velocidad:float=8):
        super().__init__(":resources:images/space_shooter/laserRed01.png",0.8)
        self.jugador = enemigo
        self.center_x = enemigo.center_x + OFFSET_X
        self.center_y = enemigo.center_y + OFFSET_Y
        #Cálculo de dirección:

        self.change_x = velocidad
        if velocidad <= 0:
            self.angle = -90
        else:
            self.angle = 90

