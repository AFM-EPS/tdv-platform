import arcade
import pathlib
#Constantes


RIGHT_FACING = 0
LEFT_FACING = 1
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent
TEXTURE_PATH = PROJECT_ROOT / "assets" / "debug" / "textures" / "debug_gun.png"
SCALE = 0.2

DISTANCIA_DEL_PERSONAJE = 50

print(TEXTURE_PATH)
class Arma(arcade.Sprite):
    def __init__(self):
        super().__init__(TEXTURE_PATH,SCALE)
        self.center_x = 300
        self.center_y = 300
        self.dist = DISTANCIA_DEL_PERSONAJE


    def flip(self, direction:int):
        if direction == RIGHT_FACING:
            self.height = abs(self.height)
        else:
            self.height = - abs(self.height)
