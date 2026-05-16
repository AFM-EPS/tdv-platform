import arcade
from character.proyectil_enemigo import Proyectil_enemigo
from character.proyectil_enemigo_andante import Proyectil_enemigo_andante

LEFT_FACING = 0
RIGHT_FACING = 1

SCALE = 0.8
#Reorganización de los enemigos andantes
MAX_REACTION_TIME = 25 #frames parado cuando llega a estar encima
MAX_BUSCA_TIME = 3 #segundos
class WalkingEnemy(arcade.Sprite):
    motor_enemigo = None
    def __init__(self,path,jugador:arcade.Sprite,scena:arcade.Scene, vida:int=100,velocidad:float=3,velocidad_disparo:float=2,vision:int=500,velocidad_proyectil:float=8):
        super().__init__(path,SCALE)
        self.jugador = jugador
        self.scena = scena
        #textura
        self.totalwidth = self.width


        # Propiedades físicas
        self.health = vida
        self.velocidad = velocidad / 2
        self.velocidad_disparo = velocidad_disparo
        self.vision = vision * 2
        self.velocidad_proyectil = velocidad_proyectil
        # lógica de IA
        self.agro = False
        self.distancia = 1000
        self.disparando = False
        self.disparo_cooldown = 5
        self.reactionT = 0
        self.busca = 0


    def update(self,delta_time):
        self.movimiento()
        self.disparo_cooldown -= delta_time
        ##Distancia
        self.distancia = ((self.jugador.center_x - self.center_x)**2 + (self.jugador.center_y - self.center_y)**2)**0.5
        ##cálculo Agro
        if self.distancia <= self.vision:
            self.agro = True
            self.busca = MAX_BUSCA_TIME
        else:
            if self.busca <= 0:
                self.agro = False
            else:
                self.busca -= delta_time
        if self.agro:
            if  self.disparo_cooldown <= 0:
                self.disparo_cooldown = self.velocidad_disparo
                self.disparar()

    def movimiento(self):
        if self.agro:
            if self.jugador.center_x - self.center_x > 12 and self.reactionT == 0:
                self.center_x += self.velocidad
                self.width =  - self.totalwidth
            elif self.jugador.center_x - self.center_x < -12 and self.reactionT == 0:
                self.center_x -= self.velocidad
                self.width = self.totalwidth
            else:
                if self.reactionT == 0:
                    self.reactionT = MAX_REACTION_TIME
                else:
                    self.reactionT -= 1

    def impactado(self, danno):
        self.health -= danno
        self.agro = True
        self.busca = MAX_BUSCA_TIME +1
        self.color = arcade.color.RED
        arcade.schedule(self.restaurar_color, 0.2) #funcion interesante para ejecutar un comando en cierto tiempo
        return self.health <= 0

    def restaurar_color(self, delta_time):
        # 3. Volver al color original (blanco significa sin tinte)
        self.color = arcade.color.WHITE

        # 4. Es MUY importante desprogramar la función, de lo contrario se ejecutará cada 0.2 segundos
        arcade.unschedule(self.restaurar_color)


    def disparar(self):
        if self.width <= 0:
            proyectil = Proyectil_enemigo_andante(self, self.velocidad_proyectil)
        else:
            proyectil = Proyectil_enemigo_andante(self, - self.velocidad_proyectil)
        self.scena.add_sprite("Enemy_bullets",proyectil)