import arcade
from character.proyectil_enemigo import Proyectil_enemigo



class Air_enemy(arcade.Sprite):
    def __init__(self,paths, jugador:arcade.Sprite,scena:arcade.Scene, vida:int=100,velocidad:float=6,velocidad_disparo:float=2,vision:int=500,velocidad_proyectil:float=8):
        super().__init__(paths)
        self.jugador = jugador
        self.scena = scena
        #Propiedades físicas
        self.health = vida
        self.velocidad = velocidad
        self.velocidad_disparo = velocidad_disparo
        self.vision = vision
        self.velocidad_proyectil = velocidad_proyectil
        #lógica de IA
        self.agro = False
        self.distancia = 1000
        self.disparando = False
        self.disparo_cooldown = 5



    def update(self,delta_time):

        self.disparo_cooldown -= delta_time
        ##Distancia
        self.distancia = ((self.jugador.center_x - self.center_x)**2 + (self.jugador.center_y - self.center_y)**2)**0.5
        ##cálculo Agro
        if self.distancia <= self.vision:
            self.agro = True
        else:
            self.agro = False
        if self.agro:
            if  self.disparo_cooldown <= 0:
                self.disparo_cooldown = self.velocidad_disparo
                self.disparar()

    def disparar(self):
        proyectil = Proyectil_enemigo(self, self.velocidad_proyectil)
        self.scena.add_sprite("Enemy_bullets",proyectil)

