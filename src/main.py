import math

from pathlib import Path

import arcade

from character.air_enemy import Air_enemy
from character.air_enemy2 import Air_enemy2
from character.final_boss import FinalBoss
#Importar Clases de otros archivos
## Reorganización de Clases
from character.player import PlayerCharacter as PlayerCharacter
from character.character import Character as Character
from character.walking_enemy import WalkingEnemy as WalkingEnemy
from character.proyectil import Proyectil as Proyectil
from character.arma import Arma as Arma
from character.teleporter_particle_system import TeleporterParticleSystem as TeleporterParticles

from gui.menu import MainMenu as MainMenu
from gui.game_over import GameOverView as GameOverView
from gui.victory import VictoryView as VictoryView
from gui.animation import Animation

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Space Escape"

PROJECT_ROOT = Path(__file__).parent.parent

# Escala sprites
TILE_SCALING = 1

# Velocidad de jugador y gravedad
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Constantes para el direccionamiento del personaje
RIGHT_FACING = 0
LEFT_FACING = 1

# Velocidad de movimiento de las plataformas móviles
MOVABLE_PLATFORM_SPEED = 0.4

# Cantidad de mapas
MAP_AMOUNT = 5





class GameView(arcade.View):
    """
    Clase principal del juego
    """

    def __init__(self):

        super().__init__()

        # Rastrear entradas
        self.arma = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False

        # Variable para guardar la textura del jugador
        self.player_texture = None

        # Variable para guardar el sprite del jugador
        self.player_sprite = None

        # Variable para guardar el motor de físicas
        self.physics_engine = None

        # Variable para guardar el Tiled Map
        self.tile_map = None

        # Variable para guardar el mapa a cargar
        self.map_num = 4

        # Variable para guardar el destino de un teleporter activado
        self.map_destination = None

        # Variable para guardar la escena
        self.scene = None

        # Variable para guardar cámara
        self.camera = None

        # Posición Y de la cámara
        self.y_camera_pos = None

        # Variable para guardar la cámara GUI
        self.gui_camera = None

        # Variable para guardar el puntaje
        self.score = 0

        # Variable para guardar el texto de puntuación
        self.score_text = None

        # Lista de gemas
        self.gem_azul = 0
        self.gem_dorada = 0
        self.gem_verde = 0

        # Variable para almacenar el fin del mapa
        self.end_of_map = 0

        # Flag para controlar si se resetea el score
        self.reset_score = True

        # Variables para controlar el disparo
        self.can_shoot = False
        self.shoot_timer = 0

        # Desplazamiento plataformas móviles
        self.movable_platforms_displacement = 0

        # Hit list de teleporters
        self.hit_list_teleporters = None

        # Sistemas de partículas
        self.particle_systems = None

        # Flag para indicar si el jugador se está teletransportando
        self.is_teleporting = None

        # Texto objetos presionables por el jugador
        self.pressable_text = arcade.Text("", 0, 0, arcade.color.WHITE, 14, anchor_x="center", font_name="Impact")
        # Letra E presionada
        self.e_pressed = False

        # Variable para almacenar si el jugador tiene arma
        self.has_gun = False

        # Variable para almacenar si se ha derrotado al final boss
        self.final_boss_defeated = None

        # Cargar texturas de gemas
        self.gem_azul_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "blue_ore.png")
        self.gem_verde_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "green_ore.png")
        self.gem_dorada_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "golden_ore.png")

        # Ruta vídeos
        self.abduction_video_path = PROJECT_ROOT / "assets" / "videos" / "animation-abduction.mov"
        self.victory_video_path = PROJECT_ROOT / "assets" / "videos" / "animation-victory.mov"
        # Ruta audio vídeos
        self.abduction_audio_path = PROJECT_ROOT / "assets" / "music" / "animation-abduction-audio.mp3"
        self.victory_audio_path = PROJECT_ROOT / "assets" / "music" / "animation-victory-audio.mp3"

        # Cargar sonidos
        self.collect_coin_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "coin1.wav")
        self.jump_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "jump1.wav")
        self.gameover_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "gameover1.wav")
        self.shoot_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "hurt5.wav")
        self.background_music = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "asteroid_runway.mp3")
        self.music_player = None
        self.step_default_music = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "step_default.mp3")
        self.walk_player = None
        self.is_walking_sound_on = False
        self.climb_player = None
        self.is_climbing_sound_on = False



        self.final_hit_platform_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "final_hit_platform.wav")
        self.hit_platform_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "hit_platform.mp3")
        self.final_hit_enemy_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "final_hit_enemy.mp3")
        self.hit_enemy_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "hit_enemy.mp3")
        self.climbing_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "climbing.mp3")
        self.player_teleporting_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "teleporting.mp3")
        self.player_teleported_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "teleported.mp3")
        self.player_damage_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "suffering_damage.mp3")
        self.music_level1 = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "music_level1.mp3")
        self.player_heal_sound = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "player_heal.mp3")
                
    def setup(self):

        # Reseteo de las variables de la trampa del mapa 4
        self.map4_trap_triggered = False
        self.map4_door_sprites = []
        self.map4_boss_enemy = None

        # Parámetros configurables de la arena del Mapa 5
        self.map5_trap_triggered = False
        self.map5_door_sprites = []
        self.map5_boss_enemy = None

        # Parámetros configurables de la arena del Mapa 4
        self.map4_arena_trigger_x = 2780
        self.map4_door_left_x = 2560
        self.map4_door_right_x = 4480

        layer_options = {
            "platforms": {
                "use_spatial_hash": True
            },
            "special_platforms": {
                "use_spatial_hash": False
            },
            "extras": {
                "use_spatial_hash": True
            },
            "ladders": {
                "use_spatial_hash": True
            },
            "teleporters": {
                "use_spatial_hash": True
            }
        }


        # Cargar el tile map
        self.tile_map = arcade.load_tilemap(
            PROJECT_ROOT / "assets" / "levels" / "maps" / f"mapa-{self.map_num}.json",
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )
        # Crear escena según el tile map
        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        # Inicializar la cámara
        self.camera = arcade.Camera2D()



        # De esta manera se evita que ciertas capas de Tiled ausentes en ciertos mapas, no den errores
        expected_layers = [
            "enemies",
            "platforms",
            "special_platforms",
            "movable_platforms",
            "destructible_platforms",
            "ores",
            "teleporters",
            "ladders",
            "player_death_zones",
            "extras",
            "Bullets",
            "Enemy_bullets",
            "pressable_objects",
        ]
        for layer in expected_layers:
            try:
                self.scene[layer]
            except KeyError:
                self.scene.add_sprite_list(layer)




        # Daño del arma y cadencia (frames entre disparo)
        self.arma = Arma(danno=25, fireRate=30)

        if self.map_num not in [1, 2]:
            self.has_gun = True

        # Crear arma y jugador
        self.scene.add_sprite("Arma", self.arma)
        self.player_sprite = PlayerCharacter(self.arma,self.camera, self.physics_engine)

        # Controlar que se muestre el arma o no
        if self.has_gun:
            self.arma.active = True
        else:
            self.player_sprite.arma.visible = False
        
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)


        # Si el jugador no puede avanzar verticalmente, la posición Y de la cámara se fijará
        self.y_camera_pos = self.tile_map.tile_height * 2 + self.player_sprite.height


        # Enemigos
        enemies_layer = self.tile_map.object_lists.get("enemies", [])

        for enemy_marker in enemies_layer:

            coordinates = self.tile_map.get_cartesian(
                enemy_marker.shape[0], enemy_marker.shape[1]
            )
            #Usamos .get para que no de excepción en caso de no encontrar, también pong casos base por si acaso
            enemy_type = enemy_marker.properties.get("type", "walking_1")
            enemy_health = enemy_marker.properties.get("health", 100)
            enemy_shot_cadence = enemy_marker.properties.get("shot_cadence", 2)
            enemy_shot_speed = enemy_marker.properties.get("shot_speed", 8)
            enemy_speed = enemy_marker.properties.get("speed", 3)
            enemy_vision = enemy_marker.properties.get("vision", 500)


            if enemy_type == "flying_1":
                enemy = Air_enemy(PROJECT_ROOT / "assets" / "sprites" / "flying_robot" / "flying_robot.png", self.player_sprite, self.scene, enemy_health, enemy_speed, enemy_shot_cadence, enemy_vision, enemy_shot_speed)
                enemy.motor_enemigo = arcade.PhysicsEnginePlatformer(  # Gravedad
                    enemy,
                    walls=self.scene["platforms"],
                    gravity_constant=0,
                    platforms=[self.scene["special_platforms"], self.scene["extras"], self.scene["teleporters"]],
                )
            elif enemy_type == "flying_2":
                enemy = Air_enemy2(PROJECT_ROOT / "assets" / "sprites" / "flying_robot2" / "flying_robot2.png", self.player_sprite, self.scene, enemy_health, enemy_speed, enemy_shot_cadence, enemy_vision, enemy_shot_speed)
                enemy.motor_enemigo = arcade.PhysicsEnginePlatformer(  # Gravedad
                    enemy,
                    walls=self.scene["platforms"],
                    gravity_constant=0,
                    platforms=[self.scene["special_platforms"], self.scene["extras"]],
                )
            elif enemy_type == "final_boss":
                # La salud especificada es de 400
                enemy_health = 400
                enemy = FinalBoss(PROJECT_ROOT / "assets" / "sprites" / "final_boss" / "final_boss.png", self.player_sprite, self.scene, enemy_health, enemy_speed, enemy_shot_cadence, enemy_vision, enemy_shot_speed)
                enemy.motor_enemigo = arcade.PhysicsEnginePlatformer(  # Gravedad
                    enemy,
                    walls=self.scene["platforms"],
                    gravity_constant=0,
                    platforms=[self.scene["special_platforms"], self.scene["extras"]],
                )


            elif enemy_type == "walking_1":
                enemy = WalkingEnemy(PROJECT_ROOT / "assets" / "sprites" / "walking_robot" / "WalkingRobot_idle.png",self.player_sprite,self.scene, enemy_health, enemy_speed, enemy_shot_cadence, enemy_vision, enemy_shot_speed)
                enemy.motor_enemigo = arcade.PhysicsEnginePlatformer( #Gravedad
                    enemy,
                    walls=self.scene["platforms"],
                    gravity_constant=GRAVITY,
                    platforms=[self.scene["special_platforms"], self.scene["extras"], self.scene["teleporters"]],
                )

            self.scene.add_sprite("enemies", enemy)

            enemy.center_x = math.floor(
                coordinates[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (coordinates[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            # Buscamos primero al enemigo que esté físicamente dentro de la arena (entre las dos compuertas).
            # Si no hay ninguno dentro del rango configurado, se hace un fallback al primer flying_2 que se encuentre.
            if enemy_type == "flying_2" and self.map_num == 4:
                if self.map4_door_left_x <= enemy.center_x <= self.map4_door_right_x:
                    self.map4_boss_enemy = enemy
                elif self.map4_boss_enemy is None:
                    # Fallback por si las coordenadas no encierran al boss inicial
                    self.map4_boss_enemy = enemy

        # Plataformas especiales (móviles / destructibles)
        for special_platform in self.scene["special_platforms"]:

            # Actualizadas algunas líneas para control de excepciones

            # En caso de plataforma destructible, se le asigna una vida
            if special_platform.properties.get("destructible", False):
                special_platform.properties["health"] = special_platform.properties.get("health",100)
                # La vida de la plataforma se asigna desde tiled
                self.scene.add_sprite("destructible_platforms", special_platform)

            if special_platform.properties.get("movable", False):
                special_platform.properties["initial_pos"] = (special_platform.center_x, special_platform.center_y)

                if special_platform.properties.get("move_on_x", False):
                    special_platform.change_x = MOVABLE_PLATFORM_SPEED
                else:
                    special_platform.change_y = MOVABLE_PLATFORM_SPEED

                self.scene.add_sprite("movable_platforms", special_platform)



        self.movable_platforms_displacement = self.tile_map.tile_height * 4


        # Lista sistemas de partículas
        self.particle_systems = []


        self.is_teleporting = False


        # Creación motor de físicas
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=[self.scene["platforms"], self.scene["special_platforms"]],
            gravity_constant=GRAVITY,
            platforms=[self.scene["extras"], self.scene["teleporters"]],
            ladders=self.scene["ladders"]
        )



        # Inicializar cámara GUI
        self.gui_camera = arcade.Camera2D()

        # Resetear puntaje si es necesario
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Mecánicas de disparo
        self.can_shoot = False
        self.shoot_timer = 0

        # Inizialización texto puntaje
        self.score_text = arcade.Text(f"Score: {self.score}{self.gem_azul}{self.gem_verde}{self.gem_dorada}", x=25, y=25, font_name="Impact")

        # Calcular borde derecho del mapa
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width)
        self.end_of_map *= self.tile_map.scaling


        # Cambio para arreglar errores
        if self.tile_map.background_color:
            self.window.background_color = self.tile_map.background_color
        else:
            # Poner un color por defecto si el mapa no lo tiene configurado
            self.window.background_color = arcade.color.SKY_BLUE
        
         # Cargar texturas de corazones
        self.heart_full_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "Corazon.png")
        self.heart_empty_texture = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "Corazon_vacio.png")
        self.player_heal = arcade.load_texture(PROJECT_ROOT / "assets" / "img" / "heal.png")

        # Crear lista de sprites para los corazones (4 corazones)
        self.heart_sprites = arcade.SpriteList()
        heart_size = 60
        spacing = 10
        total_width = 4 * heart_size + 3 * spacing
        start_x = WINDOW_WIDTH - 20 - total_width + heart_size / 2
        start_y = WINDOW_HEIGHT - 20 - heart_size / 2

        for i in range(4):
            heart = arcade.Sprite()
            heart.texture = self.heart_full_texture
            heart.width = heart_size
            heart.height = heart_size
            heart.center_x = start_x + i * (heart_size + spacing)
            heart.center_y = start_y
            self.heart_sprites.append(heart)

        # Número gemas
        self.gem_imagen_sprites = arcade.SpriteList()
        spacing = 10
        x_correct = -225
        y_correct = -20

        # Azul
        azul_size = 60
        total_width = 4 * azul_size + 3 * spacing
        start_x = 20 + x_correct + total_width + azul_size / 2
        start_y = 20 + y_correct + azul_size / 2

        gem = arcade.Sprite()
        gem.texture = self.gem_azul_texture
        gem.width = azul_size
        gem.height = azul_size
        gem.center_x = start_x + 1 * (azul_size + spacing)
        gem.center_y = start_y
        self.gem_imagen_sprites.append(gem)

        # Verde
        verde_size = 60
        total_width = 4 * verde_size + 3 * spacing
        start_x = 20 + x_correct+ total_width + verde_size / 2
        start_y = 20 + y_correct +verde_size / 2

        gem = arcade.Sprite()
        gem.texture = self.gem_verde_texture
        gem.width = verde_size
        gem.height = verde_size
        gem.center_x = start_x + 2 * (verde_size + spacing)
        gem.center_y = start_y
        self.gem_imagen_sprites.append(gem)

        # Dorada
        dorada_size = 60
        total_width = 4 * dorada_size + 3 * spacing
        start_x = 20 + x_correct + total_width + dorada_size / 2
        start_y = 20 + y_correct + dorada_size / 2

        gem = arcade.Sprite()
        gem.texture = self.gem_dorada_texture
        gem.width = dorada_size
        gem.height = dorada_size
        gem.center_x = start_x + 3 * (dorada_size + spacing)
        gem.center_y = start_y
        self.gem_imagen_sprites.append(gem)


    def on_show_view(self):

        self.setup()

        # Volúmenes
        if self.map_num == 1:
            self.music_player = self.music_level1.play(volume=0.7, loop=True)
        else:
            self.music_player = self.background_music.play(volume=0.7, loop=True)



    def on_draw(self):

        # Limpiar pantalla
        self.clear()

        # Hasta que no se carguen las cámaras no se ejecutará el resto, necesario para evitar errores
        if self.camera is None or self.gui_camera is None:
            return

        # Activar cámara
        self.camera.use()

        # Dibujar escena
        self.scene.draw()

        # Dibujar texto de objetos presionables
        self.pressable_text.draw()

        # Dibujar partículas
        for particle_system in self.particle_systems:
            particle_system.draw()

        # Activar cámara GUI
        self.gui_camera.use()

        # Dibujar texto de puntaje
        self.score_text.draw()

        # Dibujar imagenes contador de gemas
        self.gem_imagen_sprites.draw()

        # Dibujar corazones de vida
        self.draw_health_hearts()

    def draw_health_hearts(self):
        # Dibuja 4 corazones en la esquina superior derecha.
        if self.player_sprite is None:
            return

        lives = int(self.player_sprite.current_health // 25)
        # Clamp entre 0 y 4 para evitar errores si la salud está fuera de rango
        lives = max(0, min(4, lives))

        for i, heart in enumerate(self.heart_sprites):
            heart.texture = self.heart_full_texture if i < lives else self.heart_empty_texture

        self.heart_sprites.draw()   

    def on_update(self, delta_time):

        # Hasta que no se cargue el motor de físicas no se ejecutará el resto, necesario para evitar errores
        if self.physics_engine is None:
            return

        # Reducir timer de invencibilidad cada frame
        if self.player_sprite.invincible_timer > 0:
            self.player_sprite.invincible_timer -= 1
            self.player_sprite.visible = (self.player_sprite.invincible_timer // 5) % 2 == 0
        else:
            self.player_sprite.visible = True

        # Actualizar animación de escalada
        if self.physics_engine.is_on_ladder():
            self.player_sprite.climbing = True
        else:
            self.player_sprite.climbing = False


        # Lógica de disparo
        if self.can_shoot and self.player_sprite is not None:

            if self.shoot_pressed:

                if self.player_sprite.arma.active:
                    arcade.play_sound(self.shoot_sound)
                    bullet = Proyectil(self.player_sprite,self.player_sprite.aim_radians)
                    self.scene.add_sprite("Bullets", bullet)
                
                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == self.arma.fireRate:
                self.can_shoot = True
                self.shoot_timer = 0


        # Mover plataformas móviles alternando sentido de velocidad
        for movable_platform in self.scene["movable_platforms"]:

            speed = MOVABLE_PLATFORM_SPEED

            if movable_platform.properties["move_on_x"]:

                movable_platform.change_x = speed if movable_platform.change_x > 0 else -speed

                initial_pos = movable_platform.properties["initial_pos"][0]
                # Alternar sentido movimiento plataforma
                if (movable_platform.center_x >= initial_pos + self.movable_platforms_displacement) or (movable_platform.center_x <= initial_pos - self.movable_platforms_displacement): movable_platform.change_x = - movable_platform.change_x
            else:

                movable_platform.change_y = speed if movable_platform.change_y > 0 else -speed

                initial_pos = movable_platform.properties["initial_pos"][1]
                # Alternar sentido movimiento plataforma
                if (movable_platform.center_y >= initial_pos + self.movable_platforms_displacement) or (movable_platform.center_y <= initial_pos - self.movable_platforms_displacement): movable_platform.change_y = - movable_platform.change_y


        # Actualizar motores de físicas de los enemigos
        for enemy in self.scene["enemies"]:
            if isinstance(enemy, WalkingEnemy) or isinstance(enemy, Air_enemy) or isinstance(enemy, Air_enemy2) or isinstance(enemy, FinalBoss):
                if hasattr(enemy, "motor_enemigo"):
                    enemy.motor_enemigo.update()


        # Lógica de sonido al andar
        if self.player_sprite.change_x != 0 and self.physics_engine.can_jump() and not self.physics_engine.is_on_ladder():
            if not self.is_walking_sound_on:
                self.walk_player = self.step_default_music.play(loop=True, volume=1.0)
                self.is_walking_sound_on = True
        else:
            if self.is_walking_sound_on and self.walk_player is not None:
                arcade.stop_sound(self.walk_player)
                self.is_walking_sound_on = False
                self.walk_player = None


        # Lógica de sonido de escalada
        if self.physics_engine.is_on_ladder() and (self.player_sprite.change_x != 0 or self.player_sprite.change_y != 0):
            if not self.is_climbing_sound_on:
                self.climb_player = arcade.play_sound(self.climbing_sound, loop=True, volume=7.0)
                self.is_climbing_sound_on = True
        else:
            if self.is_climbing_sound_on and self.climb_player is not None:
                arcade.stop_sound(self.climb_player)
                self.climb_player = None
                self.is_climbing_sound_on = False


        # Actualizar animaciones
        self.scene.update_animation(
            delta_time,
            [
                "Player",
                "enemies",
                "ores",
                "special_platforms"
            ]
        )


        # Lógica de balas de enemigos
        for bullet in self.scene["Enemy_bullets"]:
            if getattr(bullet, "no_collision", False):
                continue

            # Remover bala si se sale del mapa
            if (bullet.right < 0) or (bullet.left > self.end_of_map):
                bullet.remove_from_sprite_lists()
                continue

            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene["platforms"],
                    self.scene["special_platforms"],
                    self.scene["Player"]
                ]
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:

                    if self.scene["Player"] in collision.sprite_lists:

                        if self.player_sprite.invincible_timer <= 0:
                            is_dead = self.player_sprite.take_damage(25)
                            arcade.play_sound(self.player_damage_sound)
                            self.player_sprite.invincible_timer = self.player_sprite.invincible_duration

                            if is_dead:
                                arcade.play_sound(self.gameover_sound)
                                game_over = GameOverView(self.map_num)

                                if self.walk_player is not None:
                                    arcade.stop_sound(self.walk_player)
                                    self.walk_player = None
                                    self.is_walking_sound_on = False

                                if self.climb_player is not None:
                                    arcade.stop_sound(self.climb_player)
                                    self.climb_player = None
                                    self.is_climbing_sound_on = False
                                self.window.show_view(game_over)
                                arcade.stop_sound(self.music_player)

                    if self.scene["destructible_platforms"] in collision.sprite_lists:

                        collision.properties["health"] -= 25
                        arcade.play_sound(self.hit_platform_sound)

                        if collision.properties["health"] <= 0:
                            collision.remove_from_sprite_lists()
                            arcade.play_sound(self.final_hit_platform_sound, volume=2.5)
                return


        # Lógica de balas del jugador
        for bullet in self.scene["Bullets"]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene["enemies"],
                    self.scene["platforms"],
                    self.scene["special_platforms"]
                ]
            )



            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:

                    if self.scene["enemies"] in collision.sprite_lists:
                        collision.impactado(25)
                        if collision.health <= 0:
                            collision.remove_from_sprite_lists()
                            arcade.play_sound(self.final_hit_enemy_sound, volume=2.5)
                        arcade.play_sound(self.hit_enemy_sound)


                    if self.scene["destructible_platforms"] in collision.sprite_lists:

                        collision.properties["health"] -= 25
                        arcade.play_sound(self.hit_platform_sound)

                        if collision.properties["health"] <= 0:
                            collision.remove_from_sprite_lists()
                            arcade.play_sound(self.final_hit_platform_sound, volume=2.5)
                return

            # Remover bala si se sale del mapa
            if (bullet.right < 0) or (bullet.left > self.end_of_map):
                bullet.remove_from_sprite_lists()

        # Lista de colisiones del jugador
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene["ores"],
                self.scene["enemies"],
                self.scene["player_death_zones"]
            ]
        )

        # Gestión de colisiones del jugador
        for collision in player_collision_list:
            if self.scene["enemies"] in collision.sprite_lists:
                if self.player_sprite.invincible_timer <= 0:
                    is_dead = self.player_sprite.take_damage(25)
                    arcade.play_sound(self.player_damage_sound)
                    self.player_sprite.invincible_timer = self.player_sprite.invincible_duration
                    if is_dead:
                        arcade.play_sound(self.gameover_sound)
                        self.background_music.stop(self.music_player)
                        game_over = GameOverView(self.map_num)
                        if self.walk_player is not None:
                            arcade.stop_sound(self.walk_player)
                            self.walk_player = None
                            self.is_walking_sound_on = False
                        if self.climb_player is not None:
                            arcade.stop_sound(self.climb_player)
                            self.climb_player = None
                            self.is_climbing_sound_on = False
                        self.window.show_view(game_over)
                        return

            elif self.scene ["player_death_zones"] in collision.sprite_lists:
                arcade.play_sound(self.gameover_sound)
                self.background_music.stop(self.music_player)
                game_over = GameOverView(self.map_num)
                if self.walk_player is not None:
                    arcade.stop_sound(self.walk_player)
                    self.walk_player = None
                    self.is_walking_sound_on = False
                if self.climb_player is not None:
                    arcade.stop_sound(self.climb_player)
                    self.climb_player = None
                    self.is_climbing_sound_on = False
                self.window.show_view(game_over)
                return

            elif self.scene["ores"] in collision.sprite_lists:
                if collision.properties.get("type") == "heart":
                    # Aumentar vida máximo hasta 100
                    self.player_sprite.current_health = min(100, self.player_sprite.current_health + 25)
                    collision.remove_from_sprite_lists()
                    arcade.play_sound(self.player_heal_sound)
                else:
                    # Si la colisión es un ore, se remueve y se añade su correspondiente valor al score
                    self.score += collision.properties["value"]
                    if (collision.properties["value"] == 10):
                        self.gem_azul += 1
                    elif (collision.properties["value"] == 100):
                        self.gem_dorada += 1
                    elif (collision.properties["value"] == 50):
                        self.gem_verde += 1

                    collision.remove_from_sprite_lists()
                    arcade.play_sound(self.collect_coin_sound)
                    self.score_text.text = f"Score: {self.score}                                   {self.gem_azul}                      {self.gem_verde}                      {self.gem_dorada}"
                    self.score_text.scale = 3.0


        # Si se puede avanzar verticalmente en el mapa, la posición en Y de la cámara variará
        if self.map_num in [2, 3, 5]:
            # Solo se actualiza la posición Y de la cámara si esta no se sale del mapa
            if (self.player_sprite.center_y <= (self.tile_map.height - 1) * self.tile_map.tile_height - WINDOW_HEIGHT / 2) and (self.player_sprite.center_y >= self.tile_map.tile_height + self.player_sprite.height / 2):
                self.y_camera_pos = self.player_sprite.position[1] + self.tile_map.tile_height + self.player_sprite.height / 2


        # Centrar la cámara en el jugador y dejarla fija cuando se acerca a los bordes del mapa para que no se salga la cámara
        if self.player_sprite.center_x <= WINDOW_WIDTH / 2:
            self.camera.position = WINDOW_WIDTH / 2, self.y_camera_pos
        elif self.player_sprite.center_x >= self.end_of_map - WINDOW_WIDTH / 2:
            self.camera.position = self.end_of_map - WINDOW_WIDTH / 2, self.y_camera_pos
        else:
            self.camera.position = self.player_sprite.position[0], self.y_camera_pos



        # Detección colisiones teleporters (como el motor de físicas interpreta los teleporters como platforms, no detectará la colisión de manera habitual, así que hay que hacer un ajuste de posición)
        self.player_sprite.center_y -= 1
        hit_list_teleporters = arcade.check_for_collision_with_list(self.player_sprite, self.scene["teleporters"])
        self.player_sprite.center_y += 1


        # Generación de partículas en caso de colisión con teleporter
        for collision in hit_list_teleporters:

            if not collision.properties["is_activated"]:
                particles = TeleporterParticles(collision.center_x, collision.center_y, PROJECT_ROOT / "assets" / "img" / "particle.png")

                self.particle_systems.append(particles)

                collision.properties["is_activated"] = True

                self.is_teleporting = True

                # Se frena al jugador antes de congelarle mediante "self.is_teleporting" para evitar bugs
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0

                self.map_destination = collision.properties["destination"]
                arcade.play_sound(self.player_teleporting_sound)


        # Teletransporte cuando finaliza la animación
        for particle_system in self.particle_systems:

            particle_system.update()

            if particle_system.is_finished():

                self.particle_systems.remove(particle_system)

                self.map_num = self.map_destination
                arcade.play_sound(self.player_teleported_sound)
                self.reset_score = False
                self.setup()

        # Lógica de la trampa de compuertas en el Mapa 4
        if self.map_num == 4:
            # Activar trigger al cruzar la zona de entrada si el boss está con vida
            if not self.map4_trap_triggered and self.player_sprite.center_x >= self.map4_arena_trigger_x:
                if self.map4_boss_enemy and self.map4_boss_enemy.health > 0:
                    self.map4_trap_triggered = True

                    # Cerrar compuerta izquierda (retroceso)
                    for y_pos in [128]:
                        door = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "metal_platform.png", scale=TILE_SCALING)
                        door.center_x = self.map4_door_left_x + 64
                        door.center_y = y_pos + 64
                        self.scene.add_sprite("platforms", door)
                        self.map4_door_sprites.append(door)

                    # Cerrar compuerta derecha (avance)
                    for y_pos in [128]:
                        door = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "metal_platform.png", scale=TILE_SCALING)
                        door.center_x = self.map4_door_right_x + 64
                        door.center_y = y_pos + 64
                        self.scene.add_sprite("platforms", door)
                        self.map4_door_sprites.append(door)

                    # Reproducir sonido de impacto de plataforma para alertar del cierre
                    if self.final_hit_platform_sound:
                        arcade.play_sound(self.final_hit_platform_sound, volume=1.5)

            # Desactivar compuertas al derrotar al air_enemy2 (boss)
            if self.map4_trap_triggered and len(self.map4_door_sprites) > 0:
                self.final_boss_defeated = True
                if self.map4_boss_enemy in self.scene["enemies"] and self.map4_boss_enemy.health > 0:
                    self.final_boss_defeated = False

                if self.final_boss_defeated:
                    for door in self.map4_door_sprites:
                        door.remove_from_sprite_lists()
                    self.map4_door_sprites.clear()

                    # Reproducir sonido de teletransporte para indicar desbloqueo
                    if self.player_teleported_sound:
                        arcade.play_sound(self.player_teleported_sound, volume=1.5)

        # Lógica de la trampa y generación del boss final en el Mapa 5
        if self.map_num == 5:
            # 1. Activar trigger al subir arriba del  (por encima de Y = 4400)
            if not self.map5_trap_triggered and self.player_sprite.center_y >= 4400:
                self.map5_trap_triggered = True

                # Generar el Boss Final
                self.map5_boss_enemy = FinalBoss(
                    PROJECT_ROOT / "assets" / "sprites" / "final_boss" / "final_boss.png",
                    self.player_sprite,
                    self.scene,
                    vida=400,
                    velocidad=6,
                    velocidad_disparo=2.0,
                    vision=800,
                    velocidad_proyectil=10
                )
                self.map5_boss_enemy.center_x = 832
                self.map5_boss_enemy.center_y = 5000
                self.map5_boss_enemy.motor_enemigo = arcade.PhysicsEnginePlatformer(
                    self.map5_boss_enemy,
                    walls=self.scene["platforms"],
                    gravity_constant=0,
                    platforms=[self.scene["special_platforms"], self.scene["extras"]],
                )
                self.scene.add_sprite("enemies", self.map5_boss_enemy)

                # Cerrar compuerta para bloquear el descenso (en Y = 4160 e Y = 4288, columna 3 que es X = 448)
                for y_pos in [4160, 4288]:
                    door = arcade.Sprite(PROJECT_ROOT / "assets" / "img" / "metal_platform.png", scale=TILE_SCALING)
                    door.center_x = 3 * 128 + 64  # 448
                    door.center_y = y_pos
                    self.scene.add_sprite("platforms", door)
                    self.map5_door_sprites.append(door)

                # Reproducir sonido de impacto de plataforma para alertar del cierre
                if self.final_hit_platform_sound:
                    arcade.play_sound(self.final_hit_platform_sound, volume=1.5)

            # 2. Desactivar compuertas al derrotar al Boss Final
            if self.map5_trap_triggered and len(self.map5_door_sprites) > 0:
                self.final_boss_defeated = True
                if self.map5_boss_enemy in self.scene["enemies"] and self.map5_boss_enemy.health > 0:
                    self.final_boss_defeated = False

                if self.final_boss_defeated:
                    for door in self.map5_door_sprites:
                        door.remove_from_sprite_lists()
                    self.map5_door_sprites.clear()

                    # Reproducir sonido de teletransporte para indicar desbloqueo
                    if self.player_teleported_sound:
                        arcade.play_sound(self.player_teleported_sound, volume=1.5)

        # Evitar que el jugador se salga del mapa
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
            self.player_sprite.change_x = 0

        if self.player_sprite.right > self.end_of_map:
            self.player_sprite.right = self.end_of_map
            self.player_sprite.change_x = 0
        


        # Colisiones objetos presionables
        pressable_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["pressable_objects"])
        
        if pressable_hit_list:

            name = pressable_hit_list[0].properties.get("name")

            # Colocar texto
            self.pressable_text.text = "Presiona E"
            self.pressable_text.x = pressable_hit_list[0].center_x
            self.pressable_text.y = pressable_hit_list[0].top + 20


            if name == "rocket_door":
                # Si es la puerta del cohete del final, se oculta el texto hasta que se derrote al final boss
                if self.final_boss_defeated: self.pressable_text.text = "Presiona E"
                else: self.pressable_text.text = ""


            # Si se presiona E
            if self.e_pressed:

                if name == "car":
                    
                    # Detener música
                    if self.music_player is not None:
                        arcade.stop_sound(self.music_player)
                        self.music_player = None
                    
                    # Detener sonido de pasos para evitar bug
                    if self.is_walking_sound_on and self.walk_player is not None:
                        arcade.stop_sound(self.walk_player)
                        self.walk_player = None
                        self.is_walking_sound_on = False

                    # Se inicia la animación de abducción y cuando acaba aparece en el mapa 2
                    next_view = GameView()
                    next_view.map_num = 2
                    self.window.show_view(Animation(next_view, self.abduction_video_path, self.abduction_audio_path))


                elif name == "gun":

                    if self.player_sprite is not None:

                        self.player_sprite.arma.active = True
                        self.has_gun = True
                        self.player_sprite.arma.visible = True

                    pressable_hit_list[0].remove_from_sprite_lists() # Quitar pistola del mapa

                elif name == "rocket_door":

                    if self.final_boss_defeated:

                        # Detener música
                        if self.music_player is not None:
                            arcade.stop_sound(self.music_player)
                            self.music_player = None

                        # Detener sonido de pasos para evitar bug
                        if self.is_walking_sound_on and self.walk_player is not None:
                            arcade.stop_sound(self.walk_player)
                            self.walk_player = None
                            self.is_walking_sound_on = False

                        # Se inicia la animación de victoria y cuando acaba se muestra la pantalla de victoria
                        next_view = VictoryView()
                        self.map_num = 1
                        self.window.show_view(Animation(next_view, self.victory_video_path, self.victory_audio_path))


                self.e_pressed = False
        else:
            self.pressable_text.text = ""
        

        # Actualizar spritelists de escena
        self.scene.update(delta_time, ["enemies", "Bullets","Enemy_bullets", "special_platforms"])

        # Actualizar motor de físicas
        self.physics_engine.update()


    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):

        # Lógica de apuntar
        # Hasta que no se declare el jugador, en los milisegundos previos puede inducir un error NoneType
        if self.player_sprite is None:
            return

        self.player_sprite.mousex = x
        self.player_sprite.mousey = y


    def process_keychange(self):

        if self.is_teleporting:
            self.player_sprite.change_x = 0
            return


        # Gestionar movimiento del jugador hacia arriba en caso de que esté o no en una escalera
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED


        # Gestionar movimiento vertical
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0


        # Gestionar movimiento horizontal
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0


    # Lógica de inputs
    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:

            # Detener música antes de ir al menú
            if self.music_player is not None:
                arcade.stop_sound(self.music_player)
                # Limpiar la referencia
                self.music_player = None
            
            menu_view = MainMenu()
            self.window.show_view(menu_view)

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.Q or key == arcade.key.SPACE:
            self.shoot_pressed = True

        
        if key == arcade.key.E:
            self.e_pressed = True


        # Procesar cambio de teclas
        self.process_keychange()


    # Lógica al soltar una tecla
    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False

        if key == arcade.key.Q or key == arcade.key.SPACE:
            self.shoot_pressed = False

        if key == arcade.key.E:
            self.e_pressed = False

        # Procesar cambio de teclas
        self.process_keychange()


def main():
    # Punto de entrada al juego
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":

    main()