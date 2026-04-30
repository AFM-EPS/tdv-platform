import arcade


#Constantes
RIGHT_FACING = 0
LEFT_FACING = 1


class Character(arcade.Sprite):
    def __init__(self, mainPath):
        super().__init__()

        self.facing_direction = RIGHT_FACING

        self.cur_texture = 0

        main_path = mainPath
        # Load textures for idle, jump, and fall states
        idle_texture = arcade.load_texture(f"{main_path}_idle.png")
        jump_texture = arcade.load_texture(f"{main_path}_jump.png")
        fall_texture = arcade.load_texture(f"{main_path}_fall.png")
        # Make pairs with left and right facing textures
        self.idle_texture_pair = idle_texture, idle_texture.flip_left_right()
        self.jump_texture_pair = jump_texture, jump_texture.flip_left_right()
        self.fall_texture_pair = fall_texture, fall_texture.flip_left_right()
        # Load textures for walking with left and right facing textures
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_walk{i}.png")
            self.walk_textures.append((texture, texture.flip_left_right()))

        self.climbing_textures = (
            arcade.load_texture(f"{main_path}_climb0.png"),
            arcade.load_texture(f"{main_path}_climb1.png")
        )

        # This variable will change dynamically and will represent the currently
        # active texture.
        self.texture = self.idle_texture_pair[0]
