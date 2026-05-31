import arcade
import math
import random

from character.misil_enemigo import Misil_enemigo

MAX_REACTION_TIME = 25  # frames parado cuando llega a estar encima
MAX_BUSCA_TIME = 5  # segundos
VELOCIDAD_PROYECTIL_BOSS = 10

class FinalBossProjectile(arcade.Sprite):
    def __init__(self, boss, orientation: float, velocidad: float = 10):
        super().__init__(":resources:images/space_shooter/laserRed01.png", 1.0)
        self.boss = boss
        self.jugador = boss.jugador
        self.center_x = boss.center_x
        self.center_y = boss.center_y
        
        # Dirección física
        self.change_x = math.cos(orientation) * velocidad
        self.change_y = math.sin(orientation) * velocidad
        
        # Ángulo visual (el sprite por defecto apunta hacia arriba, así que restamos 90 grados para orientarlo)
        self.angle = 90-(math.degrees(orientation))


class FinalBoss(arcade.Sprite):
    """
    Enemigo Boss Final volador.
    Cuenta con 400 puntos de vida y 2 fases/modos de ataque.
    """
    def __init__(self, paths, jugador: arcade.Sprite, scena: arcade.Scene, vida: int = 400, velocidad: float = 3,
                 velocidad_disparo: float = 2.0, vision: int = 800, velocidad_proyectil: float = 8):
        super().__init__(paths)
        self.jugador = jugador
        self.scena = scena
        
        # Propiedades físicas y combate
        self.health = vida
        self.max_health = vida
        self.base_velocidad = velocidad / 2
        self.velocidad = self.base_velocidad
        self.velocidad_disparo = velocidad_disparo
        self.vision = vision * 2
        self.velocidad_proyectil = velocidad_proyectil
        
        # Lógica de IA y estados
        self.agro = False
        self.distancia = 1000
        self.disparo_cooldown = 3.0
        self.reactionT = 0
        self.busca = 0
        self.tiempo_balanceo = 0.0
        
        # Sistema de fases (Fase 1: Salud > 200, Fase 2: Salud <= 200)
        self.fase = 1
        self.attack_counter = 0
        
        # Sonido de transición y explosión
        self.transition_sound = arcade.load_sound(':resources:sounds/explosion2.wav')
        self.hit_sound = arcade.load_sound(':resources:sounds/hurt1.wav')

    def update(self, delta_time: float = 0.016666666666666666, *args, **kwargs):
        self.tiempo_balanceo += delta_time
        
        # Comprobar transición de fase
        if self.fase == 1 and self.health <= 200:
            self.fase = 2
            # Aumentar velocidad un 50%
            self.velocidad = self.base_velocidad * 1.5
            # Reproducir sonido de explosión/alerta
            arcade.play_sound(self.transition_sound, volume=1.0)
            
        # Actualizar movimiento y enfriamiento de disparo
        self.movimiento()
        self.disparo_cooldown -= delta_time
        
        # Calcular distancia al jugador
        self.distancia = ((self.jugador.center_x - self.center_x) ** 2 + (
                    self.jugador.center_y - self.center_y) ** 2) ** 0.5
                    
        # Comprobar línea de visión directa
        has_vision = False
        if self.distancia <= self.vision:
            if arcade.has_line_of_sight(self.position, self.jugador.position, self.scena["platforms"], self.vision):
                has_vision = True

        # Gestión del Agro
        if has_vision:
            self.agro = True
            self.busca = MAX_BUSCA_TIME
        else:
            if self.busca <= 0:
                self.agro = False
            else:
                self.busca -= delta_time
                
        # Lógica de Ataque
        if self.agro and has_vision:
            cooldown_actual = self.velocidad_disparo
            # En fase 2, el cooldown de disparo se reduce a la mitad (doble velocidad de ataque)
            if self.fase == 2:
                cooldown_actual = self.velocidad_disparo * 0.5
                
            if self.disparo_cooldown <= 0:
                self.disparo_cooldown = cooldown_actual
                self.disparar()
                
        # Efecto visual en Fase 2 (Temblor e indicador rojo pulsante)
        if self.fase == 2:
            # Temblor aleatorio
            self.center_x += random.uniform(-2.5, 2.5)
            self.center_y += random.uniform(-2.5, 2.5)
            # Tinte rojo pulsante
            pulsing_val = int(120 + 50 * math.sin(self.tiempo_balanceo * 12.0))
            self.color = (255, pulsing_val, pulsing_val)
        else:
            self.color = arcade.color.WHITE

    def movimiento(self):
        if self.agro:
            # Movimiento horizontal: seguir al jugador
            if self.jugador.center_x - self.center_x > 15 and self.reactionT == 0:
                self.center_x += self.velocidad
            elif self.jugador.center_x - self.center_x < -15 and self.reactionT == 0:
                self.center_x -= self.velocidad
            else:
                if self.reactionT == 0:
                    self.reactionT = MAX_REACTION_TIME
                else:
                    self.reactionT -= 1

            # Movimiento vertical (acercamiento y balanceo sinusoidal)
            # En Fase 1 el balanceo es suave y a 300px por encima.
            # En Fase 2 el balanceo es más amplio e inestable, y desciende a 250px por encima del jugador.
            if self.fase == 1:
                bobbing_offset = math.sin(self.tiempo_balanceo * 3.0) * 15.0
                target_y = self.jugador.center_y + 300.0 + bobbing_offset
            else:
                bobbing_offset = math.sin(self.tiempo_balanceo * 5.5) * 35.0
                target_y = self.jugador.center_y + 250.0 + bobbing_offset

            y_diff = target_y - self.center_y
            if abs(y_diff) > 2:
                step = math.copysign(self.velocidad, y_diff)
                if abs(y_diff) < abs(step):
                    self.center_y = target_y
                else:
                    self.center_y += step
        else:
            # Balanceo suave cuando está fuera de agro (idle)
            self.center_y += math.sin(self.tiempo_balanceo * 2.0) * 0.15

    def impactado(self, danno):
        self.health -= danno
        self.agro = True
        self.busca = MAX_BUSCA_TIME + 1
        
        # Efecto de daño rápido (parpadeo rojo) si no está ya teñido permanentemente en Fase 2
        if self.fase == 1:
            self.color = arcade.color.RED
            arcade.schedule(self.restaurar_color, 0.15)
            
        arcade.play_sound(self.hit_sound, volume=0.5)
        return self.health <= 0

    def restaurar_color(self, delta_time):
        if self.fase == 1:
            self.color = arcade.color.WHITE
        arcade.unschedule(self.restaurar_color)

    def disparar(self):
        self.attack_counter += 1
        
        if self.fase == 1:
            # FASE 1: Disparo simple teledirigido directamente al jugador
            x_diff = self.jugador.center_x - self.center_x
            y_diff = self.jugador.center_y - self.center_y
            angle = math.atan2(y_diff, x_diff)
            
            proyectil = FinalBossProjectile(self, angle, self.velocidad_proyectil)
            self.scena.add_sprite("Enemy_bullets", proyectil)
        else:
            # FASE 2: Patrones de ataque avanzados alternantes
            if self.attack_counter % 2 == 0:
                # Patrón A: Misil Teleguiado
                proyectil = Misil_enemigo(self)
                self.scena.add_sprite("Enemy_bullets", proyectil)
            else:
                # Patrón B: Disparo en Abanico de 3 direcciones hacia el jugador
                x_diff = self.jugador.center_x - self.center_x
                y_diff = self.jugador.center_y - self.center_y
                base_angle = math.atan2(y_diff, x_diff)
                
                # Tres proyectiles: -15 grados, 0 grados, +15 grados
                angles = [base_angle - math.radians(15), base_angle, base_angle + math.radians(15)]
                for angle in angles:
                    proyectil = FinalBossProjectile(self, angle, self.velocidad_proyectil * 1.1)
                    self.scena.add_sprite("Enemy_bullets", proyectil)
