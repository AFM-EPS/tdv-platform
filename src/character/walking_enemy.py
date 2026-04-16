import arcade
from character.enemy import Enemy

#Reorganización de los enemigos andantes

class RobotEnemy(Enemy):
    def __init__(self):
        super().__init__("robot", "robot")
        self.health = 100


class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__("zombie", "zombie")
        self.health = 50