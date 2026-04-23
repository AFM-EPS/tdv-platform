import arcade
import math
#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1

#Velocidad!
class Proyectil_enemigo(arcade.Sprite):
    """
        DOCSTRING
        La clase es un proyectil
        La orientación debe estar en radianes

    """
    def __init__(self,enemigo,velocidad:float=8):
        super().__init__(":resources:images/space_shooter/laserBlue01.png",0.8)
        self.jugador = enemigo
        print(enemigo.center_y)
        self.center_x = enemigo.center_x
        self.center_y = enemigo.center_y
        #Cálculo de dirección:
        self.change_y = -velocidad
        self.angle = 90

