import arcade
from character.character import Character
import pathlib
#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1

class PlayerCharacter(Character):
    def __init__(self):
        super().__init__("female_adventurer", "femaleAdventurer")

        # Track extra state related to the player. We will use these for change
        # textures in animations
        self.climbing = False
        self.should_update_walk = 0


        self.mousex = 0
        self.mousey = 0
    def update_animation(self, delta_time):
        # Figure out the direction the character is facing based on the movement
        # and previous direction.
        #
        print(self.mousex, self.mousey)
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Handle animations for climbing on ladders. We use the absolute value
        # of change_y here because we don't care if the character is moving up
        # or down, the animation stays the same.
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Handling jumping animations
        if self.change_y > 0 and not self.climbing:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.climbing:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Handle idle animations
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Handle walking
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1
