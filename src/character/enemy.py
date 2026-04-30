import arcade
from character.character import Character

#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1


class Enemy(Character):
    def __init__(self, name_folder, ):
        super().__init__(name_folder)

        self.should_update_walk = 0

