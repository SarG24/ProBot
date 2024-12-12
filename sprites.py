import pygame
from pathlib import Path

images = Path("images")

tile_size = (41, 41)


class Bot(pygame.sprite.Sprite):
    """
    A customizable robot character that can move, animate, and interact with the game world.

    Attributes:
        direction (str): The current direction the bot is facing.
        last_wormhole (NoneType): The last wormhole object the bot interacted with, used to prevent immediate re-entry.
    """
    def __init__(self, skin_filename="ProBot-1.png"):
        """
        Initializes a new Bot instance with a given skin.

        Parameters:
            skin_filename (str): Filename of the bot's skin. Defaults to "ProBot-1.png".
        """

        super().__init__()
        skin_base_name = skin_filename.rsplit(".", 1)[0]
        self.direction = "up"
        self.load_skin(
            skin_base_name
        )  # This will set the initial bot_surface and bot_rect
        self.last_wormhole = None

    def load_skin(self, skin_base_name):
        """
        Loads and scales the walking animation frames for the bot's current skin.

        Parameters:
            skin_base_name (str): The base name of the skin to load frames for.
        """
        self.bot_walk = []
        walking_frame_indices = {
            "ProBot-1": ["ProBot-Walk2.png", "ProBot-Walk1.png", "ProBot-Walk3.png"],
            "ProBot-2": ["ProBot-Walk5.png", "ProBot-Walk4.png", "ProBot-Walk6.png"],
            "ProBot-3": ["ProBot-Walk8.png", "ProBot-Walk7.png", "ProBot-Walk9.png"],
            "ProBot-4": ["ProBot-Walk11.png", "ProBot-Walk10.png", "ProBot-Walk12.png"],
            "ProBot-5": ["ProBot-Walk14.png", "ProBot-Walk13.png", "ProBot-Walk15.png"],
            "ProBot-6": ["ProBot-Walk17.png", "ProBot-Walk16.png", "ProBot-Walk18.png"],
        }
        frame_filenames = walking_frame_indices.get(
            skin_base_name, walking_frame_indices["ProBot-1"]
        )

        for frame_filename in frame_filenames:
            bot_image = pygame.image.load(
                f"images/robot/{frame_filename}"
            ).convert_alpha()
            scaled_bot = pygame.transform.smoothscale(bot_image, (41, 41))
            self.bot_walk.append(scaled_bot)

        self.bot_index = 0
        self.bot_surface = self.bot_walk[self.bot_index]
        self.bot_rect = self.bot_surface.get_rect(center=(777, 405))

    def change_skin(self, new_skin):
        """
        Changes the bot's skin and updates its image and rect accordingly.

        Parameters:
            new_skin (str): The filename of the new skin to apply.
        """
        self.image = pygame.image.load(images / "robot" / new_skin).convert_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, screen):
        """
        Draws the bot on the given screen.

        Parameters:
            screen (pygame.Surface): The screen to draw the bot on.
        """
        screen.blit(self.bot_surface, self.bot_rect)

    def animate_bot(self):
        """
        Animates the bot by cycling through its walk frames.
        """
        self.bot_index += 0.1
        if self.bot_index >= len(self.bot_walk):
            self.bot_index = 0
        self.bot_surface = self.bot_walk[int(self.bot_index)]

    def turn_bot(self, num_turns):
        """
        Turns the bot a given number of 90-degree turns and updates its direction.

        Parameters:
            num_turns (int): The number of 90-degree turns to rotate the bot.
        """
        for c, image in enumerate(self.bot_walk):
            self.bot_walk[c] = pygame.transform.rotate(image, 90 * num_turns)

        if self.direction == "up":
            if num_turns % 4 == 0:
                self.direction = "up"
            elif num_turns % 3 == 0:
                self.direction = "right"
            elif num_turns % 2 == 0:
                self.direction = "down"
            else:
                self.direction = "left"

        elif self.direction == "right":
            if num_turns % 4 == 0:
                self.direction = "right"
            elif num_turns % 3 == 0:
                self.direction = "down"
            elif num_turns % 2 == 0:
                self.direction = "left"
            else:
                self.direction = "up"

        elif self.direction == "down":
            if num_turns % 4 == 0:
                self.direction = "down"
            elif num_turns % 3 == 0:
                self.direction = "left"
            elif num_turns % 2 == 0:
                self.direction = "up"
            else:
                self.direction = "right"

        elif self.direction == "left":
            if num_turns % 4 == 0:
                self.direction = "left"
            elif num_turns % 3 == 0:
                self.direction = "up"
            elif num_turns % 2 == 0:
                self.direction = "right"
            else:
                self.direction = "down"

        self.bot_surface = self.bot_walk[int(self.bot_index)]


class Wall(pygame.sprite.Sprite):
    """
    Represents a wall obstacle in the game world.
    """
    def __init__(self, pos):
        """
        Initializes a new Wall instance at the given position.

        Parameters:
            pos (tuple): The (x, y) position for the center of the wall.
        """
        super().__init__()
        self.obj = pygame.image.load(
            images / "level_assets" / "wall.png"
        ).convert_alpha()
        self.image = pygame.transform.smoothscale(self.obj, tile_size)
        self.rect = self.image.get_rect(center=pos)


class Bolt(pygame.sprite.Sprite):
    """
    Represents a collectible bolt item in the game.

    Attributes:
        obj (pygame.Surface): The loaded image of the bolt.
        image (pygame.Surface): The scaled image of the bolt to match the game's tile size.
        rect (pygame.Rect): The rectangle that defines the dimensions and position of the bolt.
    """
    def __init__(self, pos):
        """
        Initializes a new bolt at a specific position.

        Parameters:
            pos (tuple): The (x, y) position for the center of the bolt.
        """
        super().__init__()
        self.obj = pygame.image.load(
            images / "level_assets" / "bolt.png"
        ).convert_alpha()
        self.image = pygame.transform.smoothscale(self.obj, tile_size)
        self.rect = self.image.get_rect(center=pos)


class Door(pygame.sprite.Sprite):
    """
    Represents a door that can be either open or closed.

    Attributes:
        door_close (pygame.Surface): The image of the door when it is closed.
        door_open (pygame.Surface): The image of the door when it is open.
        image (pygame.Surface): The current image of the door, depending on its state.
        rect (pygame.Rect): The rectangle that defines the dimensions and position of the door.
        open (bool): Indicates whether the door is open.
    """
    def __init__(self, pos):
        """
        Initializes a new door at a specific position, starting in a closed state.

        Parameters:
            pos (tuple): The (x, y) position for the center of the door.
        """
        super().__init__()
        self.door_close = pygame.image.load(
            images / "level_assets" / "door_close.png"
        ).convert_alpha()
        self.door_open = pygame.image.load(
            images / "level_assets" / "door_open.png"
        ).convert_alpha()
        self.image = pygame.transform.smoothscale(self.door_close, tile_size)
        self.rect = self.image.get_rect(center=pos)
        self.open = False

    def openDoor(self):
        """
        Opens the door and updates its image to reflect the open state.
        """
        self.open = True
        self.image = pygame.transform.smoothscale(self.door_open, tile_size)


class DoorButton(pygame.sprite.Sprite):
    """
    Represents a button that, when pressed, can interact with other objects, such as opening a door.

    Attributes:
        pos (tuple): The position of the button.
        button1 (pygame.Surface): The image of the button when it is not pressed.
        button2 (pygame.Surface): The image of the button when it is pressed.
        image (pygame.Surface): The current image of the button.
        rect (pygame.Rect): The rectangle that defines the dimensions and position of the button.
        pressed (bool): Indicates whether the button has been pressed.
        linkedDoor (Door): A reference to the door object that the button is linked to, if any.
    """
    def __init__(self, pos):
        """
        Initializes a new button at a specific position.

        Parameters:
            pos (tuple): The (x, y) position for the center of the button.
        """
        super().__init__()
        self.pos = pos
        self.button1 = pygame.image.load(
            images / "level_assets" / "button1.png"
        ).convert_alpha()
        self.button2 = pygame.image.load(
            images / "level_assets" / "button2.png"
        ).convert_alpha()
        self.image = pygame.transform.smoothscale(self.button1, tile_size)

        self.rect = self.image.get_rect(center=pos)
        self.pressed = False
        self.linkedDoor = None

    def setPressed(self):
        """
        Marks the button as pressed and updates its image to reflect the pressed state.
        """
        self.pressed = True
        self.image = pygame.transform.smoothscale(self.button2, tile_size)
        self.rect = self.image.get_rect(center=self.pos)
        
    def un_press(self):
        self.pressed = False
        self.image = pygame.transform.smoothscale(self.button1, tile_size)
        self.rect = self.image.get_rect(center=self.pos)


class Wormhole(pygame.sprite.Sprite):
    """
    Represents a wormhole for teleporting the player or objects to different locations.

    Attributes:
        pos (tuple): The position of the wormhole.
        wormhole (pygame.Surface): The default wormhole image.
        red (pygame.Surface): The image representing an active or specific state of the wormhole.
        blue (pygame.Surface): Another state of the wormhole, possibly representing a different destination.
        image (pygame.Surface): The current image of the wormhole.
        rect (pygame.Rect): The rectangle that defines the dimensions and position of the wormhole.
        link (Wormhole): A reference to another wormhole object that this one is linked to, enabling teleportation between them.
    """
    def __init__(self, pos):
        """
        Initializes a new wormhole at a specific position.

        Parameters:
            pos (tuple): The (x, y) position for the center of the wormhole.
        """
        super().__init__()
        self.pos = pos
        self.wormhole = pygame.image.load(
            images / "level_assets" / "wormhole.png"
        ).convert_alpha()
        self.red = pygame.transform.smoothscale(
            pygame.image.load(
                images / "level_assets" / "wormhole2.png"
            ).convert_alpha(),
            tile_size,
        )
        self.blue = pygame.transform.smoothscale(
            pygame.image.load(
                images / "level_assets" / "wormhole3.png"
            ).convert_alpha(),
            tile_size,
        )
        self.image = pygame.transform.smoothscale(self.wormhole, tile_size)
        self.link = None
        self.rect = self.image.get_rect(center=pos)


class Trash(pygame.sprite.Sprite):
    """
    Represents a trash bin that can be interacted with by the player, possibly for discarding items.

    Attributes:
        closed_image (pygame.Surface): The image of the trash bin when it is closed.
        open_image (pygame.Surface): The image of the trash bin when it is open.
        image (pygame.Surface): The current image of the trash bin.
        rect (pygame.Rect): The rectangle that defines the dimensions and position of the trash bin.
    """
    def __init__(self, pos, scale=(50, 50)):  # Add a 'scale' parameter with default size
        """
        Initializes a new trash bin at a specific position, with an optional scale parameter to adjust its size.

        Parameters:
            pos (tuple): The (x, y) position for the center of the trash bin.
            scale (tuple): The (width, height) scaling factors for the trash bin. Defaults to (50, 50).
        """
        super().__init__()
        closed_bin_image = pygame.image.load(
            images / "level_assets" / "closedBin.png"
        ).convert_alpha()
        open_bin_image = pygame.image.load(
            images / "level_assets" / "openBin.png"
        ).convert_alpha()

        # Scale images to the new size
        self.closed_image = pygame.transform.smoothscale(closed_bin_image, scale)
        self.open_image = pygame.transform.smoothscale(open_bin_image, scale)
        self.image = self.closed_image
        self.rect = self.image.get_rect(center=pos)

    def open_bin(self):
        """
         Opens the trash bin and updates its image to the open state.
         """
        self.image = self.open_image

    def close_bin(self):
        """
        Closes the trash bin and updates its image back to the closed state.
        """
        self.image = self.closed_image

