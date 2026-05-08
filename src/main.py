"""
Platformer Game. 

Basado en el tutorial de arcade: https://arcade.academy/examples/platform_tutorial.html#platform-tutorial
"""
import math

from pathlib import Path

import arcade

from character.air_enemy import Air_enemy
#Importar Clases de otros archivos
## Reorganización de Clases
from character.player import PlayerCharacter as PlayerCharacter
from character.character import Character as Character
from character.walking_enemy import WalingEnemy as WalkingEnemy
from character.proyectil import Proyectil as Proyectil
from character.arma import Arma as Arma

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Constants used to track the direction a character is facing
RIGHT_FACING = 0
LEFT_FACING = 1

# Velocidad de movimiento de las plataformas móviles
MOVABLE_PLATFORM_SPEED = 1



class MainMenu(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()

        texto = arcade.Text("Main Menu - Click To Play", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, arcade.color.BLACK, font_size=30, anchor_x="center")
        texto.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Track the current state of our input
        self.arma = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False

        # Variable to hold our texture for our player
        self.player_texture = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Inicialización del motor de físicas

        self.physics_engine = None

        # Variable to hold our Tiled Map
        self.tile_map = None

        # Variable para guardar el mapa a cargar
        self.map_num = None

        # Replacing all of our SpriteLists with a Scene variable
        self.scene = None

        # A variable to store our camera object
        self.camera = None

        # Posición Y de la cámara
        self.y_camera_pos = None

        # A variable to store our gui camera object
        self.gui_camera = None

        # This variable will store our score as an integer.
        self.score = 0

        # This variable will store the text for score that we will draw to the screen.
        self.score_text = None

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Should we reset the score?
        self.reset_score = True

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        # Desplazamiento plataformas móviles
        self.movable_platforms_displacement = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.background_music = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "Asteroid_Runway.mp3")
        self.music_player = None
        self.step_default_music = arcade.load_sound(PROJECT_ROOT / "assets" / "music" / "step_default.mp3")
        self.walk_player = None
        self.is_walking_sound_on = False
    def setup(self):
        """Set up the game here. Call this function to restart the game."""
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
            }
        }

        # Seleccionar mapa (provisionalmente se hará así para el debugging)
        self.map_num = 3


        # Load our TileMap
        self.tile_map = arcade.load_tilemap(
            PROJECT_ROOT / "assets" / "levels" / "maps" / f"mapa-{self.map_num}.json",
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )
        # Create our Scene Based on the TileMap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        # Initialize our camera, setting a viewport the size of our window.
        self.camera = arcade.Camera2D()

        # En ciertos mapas no hay ciertos elementos que en otros si, para evitar errores crearemos sus SpriteLists vacías

        self.scene.add_sprite_list("enemies")

        if self.map_num in [1]:
            self.scene.add_sprite_list("special_platforms")
            self.scene.add_sprite_list("movable_platforms")
            self.scene.add_sprite_list("destructible_platforms")
            self.scene.add_sprite_list("ores")
        if self.map_num in [1, 2]:
            self.scene.add_sprite_list("ladders")
            self.scene.add_sprite_list("player_death_zones")


        self.arma = Arma(danno=25, fireRate=30) #daño del arma y cadencia (frames entre disparo)
        self.scene.add_sprite("Arma", self.arma)
        self.player_sprite = PlayerCharacter(self.arma,self.camera)
        # Provisionalmente añadiremos esto para que el personaje no se quede atrapado en la nave de la izquierda del mapa 2
        if self.map_num == 2:
            self.player_sprite.center_x = 128 * 8
        else:
            self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)


        # Si el jugador no puede avanzar verticalmente, la posición Y de la cámara se fijará
        self.y_camera_pos = self.tile_map.tile_height * 2 + self.player_sprite.height


        ###Debug




        # -- Enemies
        enemies_layer = self.tile_map.object_lists.get("enemies", [])

        for enemy_marker in enemies_layer:

            coordinates = self.tile_map.get_cartesian(
                enemy_marker.shape[0], enemy_marker.shape[1]
            )

            enemy_type = enemy_marker.properties["type"]
            enemy_health = enemy_marker.properties["health"]
            enemy_shot_cadence = enemy_marker.properties["shot_cadence"]
            enemy_shot_speed = enemy_marker.properties["shot_speed"]
            enemy_speed = enemy_marker.properties["speed"]
            enemy_vision = enemy_marker.properties["vision"]


            if enemy_type == "flying_1":
                enemy = Air_enemy(PROJECT_ROOT / "assets" / "sprites" / "flying_robot" / "flying_robot.png", self.player_sprite, self.scene, enemy_health, enemy_speed, enemy_shot_cadence, enemy_vision, enemy_shot_speed)

            elif enemy_type == "walking_1":
                enemy = WalkingEnemy(PROJECT_ROOT / "assets" / "sprites" / "walking_robot" / "WalkingRobot_idle.png",self.player_sprite,self.scene, enemy_health, enemy_speed, enemy_shot_cadence, enemy_vision, enemy_shot_speed)
                enemy.motor_enemigo = arcade.PhysicsEnginePlatformer( #Gravedad
                    enemy,
                    walls=self.scene["platforms"],
                    gravity_constant=GRAVITY,
                    platforms=[self.scene["special_platforms"], self.scene["extras"]],
                )
            
            self.scene.add_sprite("enemies", enemy)

            enemy.center_x = math.floor(
                coordinates[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (coordinates[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )



        # Plataformas especiales (móviles / destructibles)
        for special_platform in self.scene["special_platforms"]:

            # En caso de plataforma destructible, se le asigna una vida
            if special_platform.properties["destructible"]:
                special_platform.properties["health"] = 100

                self.scene.add_sprite("destructible_platforms", special_platform)
            
            if special_platform.properties["movable"]:
                special_platform.properties["initial_pos"] = (special_platform.center_x, special_platform.center_y)

                if special_platform.properties["move_on_x"]:
                    special_platform.change_x = MOVABLE_PLATFORM_SPEED
                else:
                    special_platform.change_y = MOVABLE_PLATFORM_SPEED

                self.scene.add_sprite("movable_platforms", special_platform)



        self.movable_platforms_displacement = self.tile_map.tile_height * 4

        # Create a Platformer Physics Engine, this will handle moving our
        # player as well as collisions between the player sprite and
        # whatever SpriteList we specify for the walls.
        # It is important to supply static to the walls parameter. There is a
        # platforms parameter that is intended for moving platforms.
        # If a platform is supposed to move, and is added to the walls list,
        # it will not be moved.
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.scene["platforms"],
            gravity_constant=GRAVITY,
            platforms=[self.scene["special_platforms"], self.scene["extras"]],
            ladders=self.scene["ladders"]
        )



        # Initialize our gui camera, initial settings are the same as our world camera.
        self.gui_camera = arcade.Camera2D()

        # Reset the score if we should
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        # Initialize our arcade.Text object for score
        self.score_text = arcade.Text(f"Score: {self.score}", x=0, y=5)

        # Calculate the right edge of the map in pixels
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width)
        self.end_of_map *= self.tile_map.scaling

        # Add an empty bullet SpriteList to our scene
        self.scene.add_sprite_list("Bullets")

        self.scene.add_sprite_list("Enemy_bullets")
        #cambio para arreglar errores
        if self.tile_map.background_color:
            self.window.background_color = self.tile_map.background_color
        else:
            # Pon un color por defecto si el mapa no lo tiene configurado
            self.window.background_color = arcade.color.SKY_BLUE

    def on_show_view(self):
        self.setup()        
        self.music_player = self.background_music.play(volume=0.7, loop=True)
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Hasta que no se carguen las cámaras no se ejecutará el resto, necesario para evitar errores
        if self.camera is None or self.gui_camera is None:
            return

        # Activate our camera before drawing
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate our GUI camera
        self.gui_camera.use()

        # Draw our Score
        self.score_text.draw()

    def on_update(self, delta_time):
        """Movement and Game Logic"""


        # Hasta que no se cargue el motor de físicas no se ejecutará el resto, necesario para evitar errores
        if self.physics_engine is None:
            return


        # Update our characters animation state
        if self.physics_engine.is_on_ladder():
            self.player_sprite.climbing = True
        else:
            self.player_sprite.climbing = False

        if self.can_shoot:
            if self.shoot_pressed:
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
            
            if movable_platform.properties["move_on_x"]:
                
                initial_pos = movable_platform.properties["initial_pos"][0]
                # Alternar sentido movimiento plataforma
                if (movable_platform.center_x >= initial_pos + self.movable_platforms_displacement) or (movable_platform.center_x <= initial_pos - self.movable_platforms_displacement): movable_platform.change_x = - movable_platform.change_x
            else:
                
                initial_pos = movable_platform.properties["initial_pos"][1]
                # Alternar sentido movimiento plataforma
                if (movable_platform.center_y >= initial_pos + self.movable_platforms_displacement) or (movable_platform.center_y <= initial_pos - self.movable_platforms_displacement): movable_platform.change_y = - movable_platform.change_y


        # Move the player using our physics engine
        self.physics_engine.update()
        for enemy in self.scene["enemies"]:
            if isinstance(enemy, WalkingEnemy):
                if hasattr(enemy, "motor_enemigo"):
                    enemy.motor_enemigo.update()

        # Walking sound logic
        if self.player_sprite.change_x != 0 and self.physics_engine.can_jump():
            if not self.is_walking_sound_on:
                self.walk_player = self.step_default_music.play(loop=True, volume=1.0)
                self.is_walking_sound_on = True
        else:
            if self.is_walking_sound_on and self.walk_player is not None:
                arcade.stop_sound(self.walk_player)
                self.is_walking_sound_on = False
                self.walk_player = None

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

        self.scene.update(delta_time, ["enemies", "Bullets","Enemy_bullets", "special_platforms"])

        # Sección comentada hasta que se ajusten los límites de movimiento de los enemigos

        # Keep enemies walking within their boundaries configured in Tiled
        # for enemy in self.scene["enemies"]:
        #     if enemy.right > enemy.boundary_right and enemy.change_x > 0:
        #         enemy.change_x *= -1
        #     elif enemy.left < enemy.boundary_left and enemy.change_x < 0:
        #         enemy.change_x *= -1
        for bullet in self.scene["Enemy_bullets"]:
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
                        arcade.play_sound(self.gameover_sound)
                        game_over = GameOverView()
                        self.window.show_view(game_over)
                    if self.scene["destructible_platforms"] in collision.sprite_lists:
                        collision.properties["health"] -= 25
                        if collision.properties["health"] <= 0:
                            collision.remove_from_sprite_lists()
                return





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
                        if collision.impactado(self.arma.danno):
                            collision.remove_from_sprite_lists()
                        arcade.play_sound(self.hit_sound)
                    
                    if self.scene["destructible_platforms"] in collision.sprite_lists:
                        collision.properties["health"] -= 25
                        if collision.properties["health"] <= 0:
                            collision.remove_from_sprite_lists()
                return
            #Remove bullet if it leaves the map area.
            #Bullets only travel horizontally, so we only need to check left and right.
            if (bullet.right < 0) or (bullet.left > self.end_of_map):
                bullet.remove_from_sprite_lists()

        # Lista de colisiones con enemigos y ores
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene["ores"],
                self.scene["enemies"],
                self.scene["player_death_zones"]
            ]
        )

        for collision in player_collision_list:
            if self.scene["enemies"] in collision.sprite_lists or self.scene["player_death_zones"] in collision.sprite_lists:
                arcade.play_sound(self.gameover_sound)
                self.background_music.stop(self.music_player)
                game_over = GameOverView()
                self.window.show_view(game_over)
                return
            else:
                # Si la colisión es un ore, se remueve y se añade su correspondiente valor al score
                self.score += collision.properties["value"]
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)
                self.score_text.text = f"Score: {self.score}"
        
        
        # Si se puede avanzar verticalmente en el mapa (mapa 3 de momento), la posición en Y de la cámara variará
        if self.map_num == 3:
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

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        """
            lógica de apuntaje
        """

        # Hasta que no se declare el jugador, en los milisegundos previos puede inducir un error NoneType
        if self.player_sprite is None:
            return

        self.player_sprite.mousex = x
        self.player_sprite.mousey = y


    def process_keychange(self):
        # First handle the case where we have moved up. This needs to be handled
        # differently to move the player upwards if they are on a ladder, or
        # perform a jump if they are not on a ladder. This code might look
        # different if we had a separate button for jumping, we would only need
        # to handle moving upwards if we were on a ladder for the up key then.
        # Here we also handle the case where we have moved down while on a ladder.
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Now we need a special handling of our vertical movement while we are 
        # on a ladder, but have no input specified. When we jump, the physics
        # engine takes care of resetting our vertical movement to zero once we've
        # hit the ground. However for ladders, we need to ensure that we set the
        # vertical movement back to zero if the user does not give input, otherwise
        # once a user starts climbing a ladder, they will move upwards automatically
        # until they reach the end of the ladder. You can try commenting out this
        # block to see what that effect looks like.
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Now we just handle our horizontal movement, very similar to how we
        # did before, but now just combined in our new function.
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0


    #Loógica de imputs
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.setup()

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

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

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

        self.process_keychange()


class GameOverView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):
        self.clear()

        texto = arcade.Text("Game Over - Click to Restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, arcade.color.WHITE, 30, anchor_x="center")
        texto.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

def main():
    """Main function"""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":

    # Obtenemos la ruta del proyecto utilizando PathLib,
    # necesitamos esta ruta para poder acceder a los archivos con recursos
    # de forma independiente desde donde se ejecute el script.
    PROJECT_ROOT = Path(__file__).parent.parent

    PROJECT_ROOT = Path(__file__).parent.parent
    print(f"Project root is: {PROJECT_ROOT}")

    # Ejemplo de acceso a un archivo dentro de recursos
    filetest = PROJECT_ROOT / "assets" / "dialogs.txt"
    print(f"Test file size: {filetest.stat().st_size} bytes")
    

    main()