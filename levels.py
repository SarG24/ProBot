import pygame
import pickle
import os
import pathlib
from button import Button
from code_block import (
    CodeBlock,
    MoveAndTurnBlock,
    ConditionalBlock,
    EndConditionalBlock,
)
from sprites import Bot, Wall, Bolt, DoorButton, Door, Wormhole, Trash
from pathlib import Path, WindowsPath, PosixPath

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

tile_width = 41
tile_height = 41

images = Path("images")

pixel_to_location = [
    [
        (79, 76),
        (120, 76),
        (161, 76),
        (202, 76),
        (243, 76),
        (284, 76),
        (325, 76),
        (366, 76),
        (407, 76),
        (448, 76),
        (489, 76),
        (530, 76),
        (571, 76),
        (612, 76),
        (653, 76),
        (694, 76),
        (735, 76),
        (776, 76),
    ],
    [
        (79, 117),
        (120, 117),
        (161, 117),
        (202, 117),
        (243, 117),
        (284, 117),
        (325, 117),
        (366, 117),
        (407, 117),
        (448, 117),
        (489, 117),
        (530, 117),
        (571, 117),
        (612, 117),
        (653, 117),
        (694, 117),
        (735, 117),
        (776, 117),
    ],
    [
        (79, 158),
        (120, 158),
        (161, 158),
        (202, 158),
        (243, 158),
        (284, 158),
        (325, 158),
        (366, 158),
        (407, 158),
        (448, 158),
        (489, 158),
        (530, 158),
        (571, 158),
        (612, 158),
        (653, 158),
        (694, 158),
        (735, 158),
        (776, 158),
    ],
    [
        (79, 199),
        (120, 199),
        (161, 199),
        (202, 199),
        (243, 199),
        (284, 199),
        (325, 199),
        (366, 199),
        (407, 199),
        (448, 199),
        (489, 199),
        (530, 199),
        (571, 199),
        (612, 199),
        (653, 199),
        (694, 199),
        (735, 199),
        (776, 199),
    ],
    [
        (79, 240),
        (120, 240),
        (161, 240),
        (202, 240),
        (243, 240),
        (284, 240),
        (325, 240),
        (366, 240),
        (407, 240),
        (448, 240),
        (489, 240),
        (530, 240),
        (571, 240),
        (612, 240),
        (653, 240),
        (694, 240),
        (735, 240),
        (776, 240),
    ],
    [
        (79, 281),
        (120, 281),
        (161, 281),
        (202, 281),
        (243, 281),
        (284, 281),
        (325, 281),
        (366, 281),
        (407, 281),
        (448, 281),
        (489, 281),
        (530, 281),
        (571, 281),
        (612, 281),
        (653, 281),
        (694, 281),
        (735, 281),
        (776, 281),
    ],
    [
        (79, 322),
        (120, 322),
        (161, 322),
        (202, 322),
        (243, 322),
        (284, 322),
        (325, 322),
        (366, 322),
        (407, 322),
        (448, 322),
        (489, 322),
        (530, 322),
        (571, 322),
        (612, 322),
        (653, 322),
        (694, 322),
        (735, 322),
        (776, 322),
    ],
    [
        (79, 363),
        (120, 363),
        (161, 363),
        (202, 363),
        (243, 363),
        (284, 363),
        (325, 363),
        (366, 363),
        (407, 363),
        (448, 363),
        (489, 363),
        (530, 363),
        (571, 363),
        (612, 363),
        (653, 363),
        (694, 363),
        (735, 363),
        (776, 363),
    ],
    [
        (79, 404),
        (120, 404),
        (161, 404),
        (202, 404),
        (243, 404),
        (284, 404),
        (325, 404),
        (366, 404),
        (407, 404),
        (448, 404),
        (489, 404),
        (530, 404),
        (571, 404),
        (612, 404),
        (653, 404),
        (694, 404),
        (735, 404),
        (776, 404),
    ],
]


class Tutorial:
    """
    This class handles the tutorial presentation for the game.
    
    Attributes:
        screen (pygame.Surface): The screen surface to display the tutorial images.
        images (list): A list of loaded tutorial images.
        current_image (int): The index of the current tutorial image being displayed.
        background (pygame.Surface): The background surface that the tutorial is drawn on.
        next_button (Button): Button to go to the next tutorial image.
        prev_button (Button): Button to go to the previous tutorial image.
    """
    def __init__(self, screen):
        """
        Initialize the Tutorial object with the game screen.
        
        Parameters:
            screen (pygame.Surface): The main screen surface where the tutorial will be displayed.
        """
        # Preload images as before
        self.images = [
            pygame.image.load(images / "tutorial" / f"tut{num}.png")
            for num in range(1, 5)
        ]
        self.current_image = 0  # Start with the first image
        self.screen = screen
        self.background = screen.copy()

        # Determine the size of the tutorial image to position buttons correctly
        tutorial_size = self.images[
            0
        ].get_size()  # Assuming all images are the same size
        screen_center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        # Calculate positions for the buttons
        # They are placed at the left and right side of the tutorial image
        self.next_button_position = (
            screen_center[0] + tutorial_size[0] / 2 + 15,
            screen_center[1],
        )
        self.prev_button_position = (
            screen_center[0] - tutorial_size[0] / 2 - 15,
            screen_center[1],
        )

        # Create buttons at the calculated positions
        self.next_button = Button(self.next_button_position, (40, 40), "Green", ">", 32)
        self.prev_button = Button(self.prev_button_position, (40, 40), "Red", "<", 32)

    def run(self):
        """
        Runs the tutorial sequence, displaying images and handling navigation between them.
        
        No parameters.
        
        Returns:
            None.
        """
        tutorial_running = True
        last_image_reached = (
            False  # New flag to indicate the last image has been reached
        )

        while tutorial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_button.is_clicked(event):
                        if self.current_image < len(self.images) - 1:
                            self.current_image += 1
                        elif (
                            last_image_reached
                        ):  # Check if the last image has been reached
                            tutorial_running = (
                                False  # Exit the tutorial on the next click
                            )
                        if self.current_image == len(self.images) - 1:
                            last_image_reached = True  # Set the flag to True
                    elif self.prev_button.is_clicked(event) and self.current_image > 0:
                        self.current_image -= 1
                        last_image_reached = False

            # Fill the screen with a semi-transparent surface
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            self.screen.blit(self.background, (0, 0))  # Blit the captured background
            self.screen.blit(overlay, (0, 0))  # Blit the semi-transparent overlay

            # Center the tutorial image on the screen
            image_rect = self.images[self.current_image].get_rect(
                center=(self.screen.get_width() / 2, self.screen.get_height() / 2)
            )
            self.screen.blit(self.images[self.current_image], image_rect)

            # Buttons need to be drawn with self.screen as well
            self.next_button.draw(self.screen)
            self.prev_button.draw(self.screen)

            pygame.display.flip()


class Level:
    """
    This class manages the levels in the game, including drawing the level layout,
    executing user code, and handling level completion.
    
    Attributes:
        user (User): The user object for the level.
        screen (pygame.Surface): The screen surface to display the level.
        level (str): The level identifier.
        hint (str, optional): A hint for the level.
        hint_button (Button): Button to display the hint.
    """
    def __init__(self, level, user, screen, hint=None):
        """
        Initialize the Level object with a level number, user, screen, and an optional hint.
        
        Parameters:
            level (str): The identifier for the level.
            user (User): The user playing the level.
            screen (pygame.Surface): The surface to draw the level on.
            hint (str, optional): The hint text for the level.
        """
        self.user = user
        self.screen = screen
        self.level = level
        self.pixel_count = 0
        self.obstacle_list = pygame.sprite.Group()
        self.hint = hint
        self.hint_button = Button((1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24)  # Initialize hint button
        self.background_image_filename = f"level{level}.png" if level != 'tutorial' else "game_screen.png"


        sandbox_width = 1140 - 832
        sandbox_height = 578 - 177
        sandbox_x = 832
        sandbox_y = 177

        if user and hasattr(user, "skin") and user.skin:
            bot_skin = user.skin
        else:
            bot_skin = "ProBot-1.png"  # Default skin filename with extension
        self.bot = Bot(bot_skin)

        self.scroll_surf = pygame.Surface((sandbox_width, sandbox_height * 3))
        self.scroll_surf.fill("Grey")

        self.scroll_rect = self.scroll_surf.get_rect(
            topleft=(sandbox_x, sandbox_y + 10)
        )

        # Position the trash bin in the bottom right of the sandbox
        trash_bin_pos = (
            (sandbox_x + sandbox_width - 100 // 2) + 75,
            sandbox_y + sandbox_height - 100 // 2,
        )

        # Initialize the trash bin
        self.trash_bin = Trash(trash_bin_pos, scale=(60, 60))

        self.show_hint = False

        if level == "tutorial":
            self.hint_button = Button(
                (1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24
            )

            self.layout = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]

            # Add obstacles and the bolt to the obstacle list
            for row in range(len(self.layout)):
                for col in range(len(self.layout[row])):
                    position = pixel_to_location[row][col]
                    if self.layout[row][col] == 3:
                        self.obstacle_list.add(Bolt(position))

        if level == "1":
            self.hint_button = Button(
                (1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24
            )

            # add obstacles
            self.bolt = Bolt(pixel_to_location[4][8])
            self.obstacle_list.add(self.bolt)

            # layout
            self.layout = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]

            for row in range(len(self.layout)):
                for col in range(len(self.layout[0])):
                    if self.layout[row][col] == 2:
                        self.obstacle_list.add(Wall(pixel_to_location[row][col]))
                    elif self.layout[row][col] == 3:
                        self.obstacle_list.add(Bolt(pixel_to_location[row][col]))

        if level == "2":

            self.hint_button = Button(
                (1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24
            )

            # add obstacles
            self.worm1 = Wormhole(pixel_to_location[0][0])
            self.worm2 = Wormhole(pixel_to_location[8][12])
            self.worm1.link = self.worm2
            self.worm2.link = self.worm1
            self.dbutton = DoorButton(pixel_to_location[0][14])
            self.door = Door(pixel_to_location[2][16])
            self.dbutton.linkedDoor = self.door
            self.bolt = Bolt(pixel_to_location[2][17])

            self.obstacle_list.add(self.door)
            self.obstacle_list.add(self.dbutton)
            self.obstacle_list.add(self.bolt)
            self.obstacle_list.add(self.worm1)
            self.obstacle_list.add(self.worm2)

            # layout
            self.layout = [
                [self.worm1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, self.dbutton, 0, 0, 0,],
                [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2],
                [0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, self.door, 3],
                [0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2],
                [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0, 2, 0, 0, 0, 0],
                [2, 0, 2, 2, 0, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 0, 0, 0],
                [2, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0],
                [2, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 0, self.worm2, 2, 0, 0, 0, 0],
            ]

            for row in range(len(self.layout)):
                for col in range(len(self.layout[0])):
                    if self.layout[row][col] == 2:
                        self.obstacle_list.add(Wall(pixel_to_location[row][col]))
                    elif self.layout[row][col] == 3:
                        self.obstacle_list.add(Bolt(pixel_to_location[row][col]))

        if level == "3":
            self.hint_button = Button(
                (1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24
            )

            self.layout = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0],
                [0, 2, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0],
                [0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            ]

            for row in range(len(self.layout)):
                for col in range(len(self.layout[0])):
                    if self.layout[row][col] == 2:
                        self.obstacle_list.add(Wall(pixel_to_location[row][col]))
                    elif self.layout[row][col] == 3:
                        self.obstacle_list.add(Bolt(pixel_to_location[row][col]))
        if level == "4":
            self.hint_button = Button(
                (1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24
            )

            # add obstacles
            self.dbutton1 = DoorButton(pixel_to_location[0][3])
            self.dbutton2 = DoorButton(pixel_to_location[0][17])
            self.dbutton3 = DoorButton(pixel_to_location[5][3])
            self.dbutton4 = DoorButton(pixel_to_location[5][17])
            self.door1 = Door(pixel_to_location[3][7])
            self.door2 = Door(pixel_to_location[3][8])
            self.door3 = Door(pixel_to_location[3][9])
            self.door4 = Door(pixel_to_location[3][10])
            self.dbutton1.linkedDoor = self.door1
            self.dbutton2.linkedDoor = self.door2
            self.dbutton3.linkedDoor = self.door3
            self.dbutton4.linkedDoor = self.door4
            self.worm1 = Wormhole(pixel_to_location[8][14])
            self.worm2 = Wormhole(pixel_to_location[8][3])
            self.worm1.link = self.worm2
            self.worm2.link = self.worm1
            self.worm3 = Wormhole(pixel_to_location[8][0])
            self.worm4 = Wormhole(pixel_to_location[3][17])
            self.worm3.image = self.worm3.blue
            self.worm4.image = self.worm4.blue
            self.worm3.link = self.worm4
            self.worm4.link = self.worm3
            self.worm5 = Wormhole(pixel_to_location[3][14])
            self.worm6 = Wormhole(pixel_to_location[3][3])
            self.worm5.image = self.worm5.red
            self.worm6.image = self.worm6.red
            self.worm5.link = self.worm6
            self.worm6.link = self.worm5
            self.worm7 = Wormhole(pixel_to_location[3][0])
            self.worm8 = Wormhole(pixel_to_location[6][10])
            self.worm7.link = self.worm8
            self.worm8.link = self.worm7
            self.bolt = Bolt(pixel_to_location[6][7])

            self.obstacle_list.add(self.door1)
            self.obstacle_list.add(self.door2)
            self.obstacle_list.add(self.door3)
            self.obstacle_list.add(self.door4)
            self.obstacle_list.add(self.dbutton1)
            self.obstacle_list.add(self.dbutton2)
            self.obstacle_list.add(self.dbutton3)
            self.obstacle_list.add(self.dbutton4)
            self.obstacle_list.add(self.bolt)
            self.obstacle_list.add(self.worm1)
            self.obstacle_list.add(self.worm2)
            self.obstacle_list.add(self.worm3)
            self.obstacle_list.add(self.worm4)
            self.obstacle_list.add(self.worm5)
            self.obstacle_list.add(self.worm6)
            self.obstacle_list.add(self.worm7)
            self.obstacle_list.add(self.worm8)

            self.layout = [
                [
                    0,
                    0,
                    0,
                    self.dbutton1,
                    2,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    2,
                    0,
                    0,
                    0,
                    self.dbutton2,
                ],
                [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0],
                [
                    self.worm7,
                    0,
                    0,
                    self.worm6,
                    2,
                    0,
                    2,
                    self.door1,
                    self.door2,
                    self.door3,
                    self.door4,
                    2,
                    0,
                    2,
                    self.worm5,
                    0,
                    0,
                    self.worm4,
                ],
                [2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2],
                [
                    0,
                    0,
                    0,
                    self.dbutton3,
                    2,
                    0,
                    2,
                    0,
                    2,
                    2,
                    0,
                    2,
                    0,
                    2,
                    0,
                    0,
                    0,
                    self.dbutton4,
                ],
                [0, 0, 0, 0, 2, 0, 2, 3, 2, 2, self.worm8, 2, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0],
                [
                    self.worm3,
                    0,
                    0,
                    self.worm2,
                    2,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    2,
                    self.worm1,
                    0,
                    0,
                    0,
                ],
            ]
            for row in range(len(self.layout)):
                for col in range(len(self.layout[0])):
                    if self.layout[row][col] == 2:
                        self.obstacle_list.add(Wall(pixel_to_location[row][col]))
                    elif self.layout[row][col] == 3:
                        self.obstacle_list.add(Bolt(pixel_to_location[row][col]))

        if level == "5":
            self.hint_button = Button(
                (1200 - 90, 30), (80, 30), "Light Blue", "Hint", 24
            )

            # add obstacles
            self.dbutton0 = DoorButton(pixel_to_location[3][8])
            self.door1 = Door(pixel_to_location[3][1])
            self.dbutton0.linkedDoor = self.door1
            self.worm1 = Wormhole(pixel_to_location[1][1])
            self.worm2 = Wormhole(pixel_to_location[2][3])
            self.worm1.link = self.worm2
            self.worm2.link = self.worm1

            self.obstacle_list.add(self.door1)
            self.obstacle_list.add(self.dbutton0)
            self.obstacle_list.add(self.worm1)
            self.obstacle_list.add(self.worm2)

            self.layout = [
                [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, self.worm1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 2, self.worm2, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [2, 6, 2, 0, 0, 8, 8, 8, self.dbutton0, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [2, 0, 2, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [2, 3, 2, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            ]

            for row in range(len(self.layout)):
                for col in range(len(self.layout[0])):
                    if self.layout[row][col] == 2:
                        self.obstacle_list.add(Wall(pixel_to_location[row][col]))
                    elif self.layout[row][col] == 3:
                        self.obstacle_list.add(Bolt(pixel_to_location[row][col]))
                    elif self.layout[row][col] == 8:
                        db = DoorButton(pixel_to_location[row][col])
                        self.layout[row][col] = db
                        self.obstacle_list.add(db)

    def display_hint(self, screen):
        """
        Display the hint on the screen if the hint button is toggled.
        
        Parameters:
            screen (pygame.Surface): The screen surface to display the hint on.
            
        Returns:
            None.
        """
        if self.show_hint:
            hint_surface = pygame.Surface((204, 104))  # Adding 4 for the outline
            hint_surface.fill("black")
            pygame.draw.rect(hint_surface, "white", (2, 2, 200, 100))

            hint_font = pygame.font.SysFont(None, 24)

            # Break the hint into lines that fit the width of the hint box
            words = self.hint.split(" ")
            lines = []
            while words:
                line = ""
                while words and hint_font.size(line + words[0])[0] <= 196:
                    line += words.pop(0) + " "
                lines.append(line)

            # Blit each line to the hint_surface
            y = 10
            for line in lines:
                hint_text = hint_font.render(line, True, (0, 0, 0))
                hint_surface.blit(hint_text, (10, y))
                y += hint_font.get_height()

            hint_popup_rect = hint_surface.get_rect(topright=(1200 - 10, 50))
            screen.blit(hint_surface, hint_popup_rect)

    # displays the pause menu
    def pause(self, screen):
        """
        Displays the pause menu during the level.
        
        Parameters:
            screen (pygame.Surface): The surface on which to display the pause menu.
            
        Returns:
            None.
        """
        paused = True
        pause_menu = pygame.Surface((300, 300))
        pause_menu.fill("grey")

        x_button = Button((470, 170), (40, 40), "red", "X", 32)
        exit_button = Button((600, 375), (300, 40), "red", "Return to Level Select", 32)
        main_menu_button = Button(
            (600, 420), (300, 40), "red", "Main Menu", 32
        )  # position still needs adjustment

        returninghome = False

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    pygame.quit()
                    exit()
                if x_button.is_clicked(event):
                    paused = False
                if exit_button.is_clicked(event):
                    paused = False
                    # Perform action to return to level select, such as returning True
                    return "level_select"
                if main_menu_button.is_clicked(event):
                    paused = False
                    # Call the main menu function or return a specific value to go to the main menu
                    returninghome = True
                    return "main_menu"

            screen.blit(pause_menu, (450, 150))
            x_button.draw(screen)
            exit_button.draw(screen)
            main_menu_button.draw(screen)

            pygame.display.update(450, 150, 300, 300)
        return False

    def get_user_code(self, start_block, block_list):
        """
        Connects the user's blocks of code starting from the 'start_block'.
        
        Parameters:
            start_block (CodeBlock): The starting block of user code.
            block_list (pygame.sprite.Group): Group of all code blocks used in the level.
            
        Returns:
            None.
        """
        for b in block_list:
            b.next = None

        start_conntected = False
        for block in block_list:
            if start_block.obj_rect.bottom == block.obj_rect.top:
                start_conntected = True
                start_block.next = block
                
        for block in block_list:
            if block.next == None:
                for block2 in block_list:
                     if block.obj_rect.bottom == block2.obj_rect.top and block.next == None and not block.locked and not block2.locked:
                        block.next = block2
                    
        temp = start_block
        while temp != None:
            temp = temp.next

        if not start_conntected:
            start_block.next = None

    def get_end_block(self, start_block):
        """
        Finds the corresponding end block for a given control structure block in user code.
        
        Parameters:
            start_block (CodeBlock): The starting block for which to find the matching end block.
        
        Returns:
            CodeBlock: The end block corresponding to the given start block.
        
        Raises:
            Exception: If the corresponding end block cannot be found.
        """
        looking_for = start_block.command
        curr_block = start_block
        if_count = 0
        else_count = 0
        while_count = 0
        for_count = 0

        while curr_block != None:

            if looking_for == "if":
                if curr_block.command == "if":
                    if_count += 1
                elif curr_block.command == "endif":
                    if if_count == 1:
                        return curr_block
                    else:
                        if_count -= 1

            elif looking_for == "else":
                if curr_block.command == "else":
                    else_count += 1
                elif curr_block.command == "endelse":
                    if else_count == 1:
                        return curr_block
                    else:
                        else_count -= 1

            elif looking_for == "while":
                if curr_block.command == "while":
                    while_count += 1
                elif curr_block.command == "endwhile":
                    if while_count == 1:
                        curr_block.return_to = start_block
                        return curr_block
                    else:
                        while_count -= 1
                        
            elif looking_for == "for":
                if curr_block.command == "for":
                    for_count += 1
                elif curr_block.command == "endfor":
                    if for_count == 1:
                        curr_block.return_to = start_block
                        return curr_block
                    else:
                        for_count -= 1

            curr_block = curr_block.next

        raise Exception("Missing end block")

    def get_bot_position(self):
        """
        Calculates the current grid position of the bot based on its pixel position.
        
        Returns:
            tuple: A tuple of the form (row_index, column_index) representing the bot's position.
        """
        return (
            int(((self.bot.bot_rect.centery + 20) / tile_height) - 2),
            int(((self.bot.bot_rect.centerx + 20) / tile_width) - 2),
        )

    def next_tile_is_open(self, layout, bot_direction, bot_pos):
        """
        Determines if the next tile in the direction the bot is facing is open and can be moved onto.
        
        Parameters:
            layout (list of lists): The level layout matrix.
            bot_direction (str): The current direction the bot is facing.
            bot_pos (tuple): The current grid position of the bot.
        
        Returns:
            bool: True if the next tile is open, False otherwise.
        """
        if bot_direction == "up":
            if self.bot.bot_rect.y == 57:
                return False
            if isinstance(layout[bot_pos[0] - 1][bot_pos[1]], Door):
                return layout[bot_pos[0] - 1][bot_pos[1]].open
            return layout[bot_pos[0] - 1][bot_pos[1]] != 2
        elif bot_direction == "down":
            if self.bot.bot_rect.y == 385:
                return False
            if isinstance(layout[bot_pos[0] + 1][bot_pos[1]], Door):
                return layout[bot_pos[0] + 1][bot_pos[1]].open
            return layout[bot_pos[0] + 1][bot_pos[1]] != 2
        elif bot_direction == "left":
            if self.bot.bot_rect.x == 60:
                return False
            if isinstance(layout[bot_pos[0]][bot_pos[1] - 1], Door):
                return layout[bot_pos[0]][bot_pos[1] - 1].open
            return layout[bot_pos[0]][bot_pos[1] - 1] != 2
        elif bot_direction == "right":
            if self.bot.bot_rect.x == 757:
                return False
            if isinstance(layout[bot_pos[0]][bot_pos[1] + 1], Door):
                return layout[bot_pos[0]][bot_pos[1] + 1].open
            return layout[bot_pos[0]][bot_pos[1] + 1] != 2

    def check_interactables(self, layout, bot_pos, screen):
        """
        Checks if the bot is currently on an interactable object and performs the necessary action.
        
        Parameters:
            layout (list of lists): The level layout matrix.
            bot_pos (tuple): The current grid position of the bot.
            screen (pygame.Surface): The screen surface to display any changes.
            
        Returns:
            None.
        """
        if isinstance(layout[bot_pos[0]][bot_pos[1]], DoorButton):
            button = layout[bot_pos[0]][bot_pos[1]]
            button.setPressed()
            screen.blit(button.image, button.rect)
            if button.linkedDoor is not None:
                button.linkedDoor.openDoor()
                screen.blit(button.linkedDoor.image, button.linkedDoor.rect)
        if isinstance(layout[bot_pos[0]][bot_pos[1]], Wormhole):
            current_wormhole = layout[bot_pos[0]][bot_pos[1]]
            if (
                self.bot.last_wormhole != current_wormhole
            ):  # Check if different from the last wormhole
                worm1 = current_wormhole
                worm2 = worm1.link
                self.bot.bot_rect.center = worm2.pos
                screen.blit(self.bot.bot_surface, self.bot.bot_rect)
                self.bot.last_wormhole = worm2  # Update last used wormhole
                self.pixel_count = 0
                self.move_count = 0

    def level_complete_screen(self, screen):
        """
        Displays the level complete screen and allows the user to return to the level selection screen.
        
        Parameters:
            screen (pygame.Surface): The screen surface where the completion screen will be displayed.
        
        Returns:
            str: A string "level_select" if the user chooses to return to the level select screen.
        """
        pause_menu = pygame.Surface((500, 500))
        pause_menu.fill("grey")

        font = pygame.font.SysFont('Arial', 55)
        text_surface = font.render('Level Complete!', True, (0, 0, 0))

        exit_button = Button((600, 375), (500, 60), "blue", "Return to Level Select", 40)

        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    pygame.quit()
                    exit()
                if exit_button.is_clicked(event):
                    paused = False
                    return "level_select"

            self.screen.blit(pause_menu, (350, 50))
            self.screen.blit(text_surface,(410,80))
            exit_button.draw(self.screen)

            pygame.display.update()

        return False
    
    def run_level(self, screen):
        """
        Main loop for running the gameplay of a level. Handles the user code execution,
        animates the bot, checks for completion, and manages user interactions.
        
        Parameters:
            screen (pygame.Surface): The screen surface where the level is being run.
            
        Returns:
            str: A string representing the next action (e.g., "level_select", "main_menu") if any.
        """
        running = True
        clock = pygame.time.Clock()

        background_image_path = images / "menus" / self.background_image_filename
        background_image = pygame.image.load(background_image_path).convert_alpha()
        background_image = pygame.transform.scale(background_image, (1200, 600)) 
        user_code_running = False
        self.pixel_count = 0
        self.move_count = 0
        has_moved = False

        # buttons
        pause_button = Button((20, 20), (40, 40), "Grey", "P", 32)
        run_button = Button((1000, 200), (40, 20), "Green", "start", 22)
        stop_button = Button((1100, 200), (40, 20), "Red", "stop", 22)
        reset_all_button = Button((1165, 220), (40, 20), "Red", "all", 22)

        

        scroll_up_button = Button((1155, 390), (20, 20), "Grey", "^", 22)
        scroll_down_button = Button((1155, 410), (20, 20), "Grey", "v", 22)

        button_list = []
        button_list.append(pause_button)
        button_list.append(run_button)
        button_list.append(stop_button)
        button_list.append(reset_all_button)

        button_list.append(scroll_up_button)
        button_list.append(scroll_down_button)
        
        if self.user.type == 2:
            load_auto_fill_button = Button((1165, 280), (40, 20), "Light Blue", "load", 22)
            save_auto_fill_button = Button((1165, 310), (40, 20), "Light Blue", "save", 22)

            button_list.append(load_auto_fill_button)
            button_list.append(save_auto_fill_button)

        

        # background
        level_surface = pygame.image.load(
            images / "menus" / "game_screen.png"
        ).convert()

        initial_positions = {
            "move": (120, 515),
            "turn": (245, 515),
            "if": (370, 515),
            "endif": (495, 515),
            "else": (620, 515),
            "endelse": (745, 515),
            "while": (120, 560),
            "endwhile": (245, 560),
            "for": (370, 560),
            "endfor": (495, 560),
        }

        # code blocks
        move_block = MoveAndTurnBlock(
            images / "blocks" / "move.png", initial_positions["move"], "move"
        )

        turn_block = MoveAndTurnBlock(
            images / "blocks" / "turn.png", initial_positions["turn"], "turn"
        )

        if_block = ConditionalBlock(
            images / "blocks" / "if.png", initial_positions["if"], "if"
        )
        end_if_block = EndConditionalBlock(
            images / "blocks" / "end_if.png", initial_positions["endif"], "endif"
        )

        else_block = ConditionalBlock(
            images / "blocks" / "else.png", initial_positions["else"], "else"
        )
        end_else_block = EndConditionalBlock(
            images / "blocks" / "end_else.png", initial_positions["endelse"], "endelse"
        )

        while_block = ConditionalBlock(
            images / "blocks" / "while.png", initial_positions["while"], "while"
        )
        end_while_block = EndConditionalBlock(
            images / "blocks" / "end_while.png",
            initial_positions["endwhile"],
            "endwhile",
        )

        for_block = ConditionalBlock(
            images / "blocks" / "for.png", initial_positions["for"], "for"
        )
        end_for_block = EndConditionalBlock(
            images / "blocks" / "end_for.png", initial_positions["endfor"], "endfor"
        )

        start_block = CodeBlock(images / "blocks" / "start.png", (890, 280), "start")

        block_list_1 = pygame.sprite.Group()
        block_list_1.add(move_block)
        block_list_1.add(turn_block)
        block_list_1.add(if_block)
        block_list_1.add(end_if_block)
        block_list_1.add(else_block)
        block_list_1.add(end_else_block)
        block_list_1.add(while_block)
        block_list_1.add(end_while_block)
        block_list_1.add(for_block)
        block_list_1.add(end_for_block)

        active_block = None

        font = pygame.font.SysFont(None, 30)
        show_message = False
        message_timer = 0
        message_text = ""  # To hold the custom message
        
        while running:
            screen.fill("white")
            screen.blit(self.scroll_surf, self.scroll_rect)   
            #background_image = pygame.image.load("images/menus/game_screen.png").convert_alpha()
            
            block_list_1.update(screen)
            start_block.update(screen)

            screen.blit(background_image, (0, 0))

            # Load the background image at the beginning of the run_level method

            self.hint_button.draw(screen)

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.pause(screen):
                            running = False
                            break
                    elif event.key == pygame.K_r:
                        self.get_user_code(start_block, block_list_1)
                        user_code_running = True
                        temp_block = start_block.next

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hint_button.is_clicked(event):
                        self.show_hint = not self.show_hint

                    if event.button == 1:

                        if pause_button.is_clicked(event):
                            action = self.pause(screen)
                            if action:
                                return action  # Pass the action up to the caller

                        if run_button.is_clicked(event):
                            self.get_user_code(start_block, block_list_1)
                            for button in self.obstacle_list:
                                if type(button) is DoorButton:
                                    button.un_press()
                            user_code_running = True
                            temp_block = start_block.next

                        if stop_button.is_clicked(event):
                            user_code_running = False
                            self.pixel_count = 0
                            self.move_count = 0
                            self.bot = Bot()

                        if reset_all_button.is_clicked(event):
                            user_code_running = False
                            self.pixel_count = 0
                            self.move_count = 0
                            self.bot = Bot()
                            for block in block_list_1:
                                if not block.locked:
                                    block_list_1.remove(block)
                        
                        try:
                            if load_auto_fill_button.is_clicked(event):
                                if self.scroll_rect.y == 187:
                                    self.pixel_count = 0
                                    self.move_count = 0
                                    block_list_1.empty()
                                    temp_list = []
                                    if os.name == 'nt':
                                        path = WindowsPath(f"block_list_{self.level}.pickle")
                                    else:
                                        path = PosixPath(f"block_list_{self.level}.pickle")
                                    with open(
                                        path, "rb"
                                    ) as file:
                                        while True:
                                            try:
                                                temp_list.append(pickle.load(file))

                                            except EOFError:
                                                break

                                    for list in temp_list:
                                        if list[2] == "move":
                                            new_block = MoveAndTurnBlock(
                                                images / "blocks" / "move.png",
                                                list[1],
                                                list[2],
                                            )
                                            new_block.input_box.user_text = list[3]
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "turn":
                                            new_block = MoveAndTurnBlock(
                                                images / "blocks" / "turn.png",
                                                list[1],
                                                list[2],
                                            )
                                            new_block.input_box.user_text = list[3]
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "if":
                                            new_block = ConditionalBlock(
                                                images / "blocks" / "if.png",
                                                list[1],
                                                list[2],
                                            )
                                            new_block.drop_down1.main = list[3]
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "while":
                                            new_block = ConditionalBlock(
                                                images / "blocks" / "while.png",
                                                list[1],
                                                list[2],
                                            )
                                            new_block.drop_down1.main = list[3]
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "else":
                                            new_block = ConditionalBlock(
                                                images / "blocks" / "else.png",
                                                list[1],
                                                list[2],
                                            )
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "for":
                                            new_block = ConditionalBlock(
                                                images / "blocks" / "for.png",
                                                list[1],
                                                list[2],
                                            )
                                            new_block.drop_down1.main = list[3]
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "endif":
                                            new_block = EndConditionalBlock(
                                                images / "blocks" / "end_if.png",
                                                list[1],
                                                list[2],
                                            )
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "endwhile":
                                            new_block = EndConditionalBlock(
                                                images / "blocks" / "end_while.png",
                                                list[1],
                                                list[2],
                                            )
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == "endelse":
                                            new_block = EndConditionalBlock(
                                                images / "blocks" / "end_else.png",
                                                list[1],
                                                list[2],
                                            )
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        elif list[2] == list[2] == "endfor":
                                            new_block = EndConditionalBlock(
                                                images / "blocks" / "end_for.png",
                                                list[1],
                                                list[2],
                                            )
                                            if (
                                                new_block.position
                                                != initial_positions[new_block.command]
                                            ):
                                                new_block.locked = False

                                        block_list_1.add(new_block)

                                else:
                                    show_message = True
                                    message_timer = pygame.time.get_ticks()
                                    message_text = "must scroll to top before loading"

                            if save_auto_fill_button.is_clicked(event):
                                if self.scroll_rect.y == 187:
                                    with open(
                                        f"block_list_{self.level}.pickle", "wb"
                                    ) as file:
                                        for block in block_list_1:
                                            if type(block) is MoveAndTurnBlock:
                                                attributes = [
                                                    block.image,
                                                    block.obj_rect.midbottom,
                                                    block.command,
                                                    block.input_box.user_text,
                                                ]

                                            elif (
                                                type(block) is ConditionalBlock
                                                and block.command != "else"
                                            ):
                                                attributes = [
                                                    block.image,
                                                    block.obj_rect.midbottom,
                                                    block.command,
                                                    block.drop_down1.main,
                                                ]

                                            else:
                                                attributes = [
                                                    block.image,
                                                    block.obj_rect.midbottom,
                                                    block.command,
                                                ]

                                            pickle.dump(
                                                attributes,
                                                file,
                                                protocol=pickle.HIGHEST_PROTOCOL,
                                            )


                                else:
                                    show_message = True
                                    message_timer = pygame.time.get_ticks()
                                    message_text = "must scroll to top before saving"
                        
                        except UnboundLocalError:
                            pass

                        if scroll_up_button.is_clicked(event):
                            if self.scroll_rect.y < 187:
                                start_block.obj_rect.y += 40
                                self.scroll_rect.y += 40
                                for block in block_list_1:
                                    if self.scroll_rect.contains(block.obj_rect):
                                        block.obj_rect.y += 40

                        if scroll_down_button.is_clicked(event):
                            if self.scroll_rect.y > -613:
                                start_block.obj_rect.y -= 40
                                self.scroll_rect.y -= 40
                                for block in block_list_1:
                                    if self.scroll_rect.contains(block.obj_rect):
                                        block.obj_rect.y -= 40

                        for block in block_list_1:
                            if block.obj_rect.collidepoint(event.pos):
                                active_block = block

                for block in block_list_1:
                    if type(block) is not EndConditionalBlock and block.command != "else":
                        num_entered = block.input_box.take_input(event)
                
                        if type(block) is ConditionalBlock :
                            selected_option = block.drop_down1.update(event)
                            if selected_option >= 0:
                                block.drop_down1.main = block.drop_down1.options[selected_option]
                                    
                            if num_entered:
                                block.drop_down1.main = block.input_box.user_text

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:

                        # Remove the block if it's dropped over the trash bin
                        if (
                            self.trash_bin.rect.collidepoint(event.pos)
                            and active_block is not None
                        ):
                            block_list_1.remove(active_block)
                            active_block = None
                        self.trash_bin.close_bin()  # Close the trash bin when the mouse button is released
                        for block in block_list_1:
                            # checks if the block is close to the start block
                            # 'connects' them if they are close
                            if (
                                start_block.obj_rect.bottom - 20 <= block.obj_rect.top
                                and start_block.obj_rect.bottom + 20
                                >= block.obj_rect.top
                            ):
                                if (
                                    start_block.obj_rect.centerx - 50
                                    <= block.obj_rect.centerx
                                    and start_block.obj_rect.centerx + 50
                                    >= block.obj_rect.centerx
                                ):
                                    block.obj_rect.top = start_block.obj_rect.bottom
                                    block.obj_rect.centerx = (
                                        start_block.obj_rect.centerx
                                    )
                            for block2 in block_list_1:
                                if block.obj_rect.center == block2.obj_rect.center and block != block2:
                                    for b in block_list_1:
                                        if b.obj_rect.centery >= block2.obj_rect.centery and not b.locked and block2 != b:
                                            b.obj_rect.y += 40
                                # checks if blocks are close to other blocks
                                if (
                                    block.obj_rect.bottom - 20 <= block2.obj_rect.top
                                    and block.obj_rect.bottom + 20
                                    >= block2.obj_rect.top
                                    and (not block2.locked and not block.locked)
                                ):
                                    if (
                                        block.obj_rect.centerx - 50
                                        <= block2.obj_rect.centerx
                                        and block.obj_rect.centerx + 50
                                        >= block2.obj_rect.centerx
                                    ):
                                        block2.obj_rect.top = block.obj_rect.bottom
                                        block2.obj_rect.centerx = block.obj_rect.centerx
                                        

                        active_block = None
                        has_moved = False

                if event.type == pygame.MOUSEMOTION:
                    if active_block != None:
                        # duplicates the move block from the block selection part
                        if (
                            active_block.obj_rect.midbottom
                            == initial_positions[active_block.command]
                        ):
                            new_block = active_block.duplicate()
                            new_block.locked = True
                            block_list_1.add(new_block)
                            active_block.obj_rect.move_ip(event.rel)
                            active_block.locked = False
                        else:
                            active_block.obj_rect.move_ip(event.rel)


                    if active_block is not None:
                        # Open the trash bin if a block is dragged over it
                        if self.trash_bin.rect.collidepoint(event.pos):
                            self.trash_bin.open_bin()
                        else:
                            self.trash_bin.close_bin()

            if self.show_hint:
                self.display_hint(screen)

            screen.blit(self.trash_bin.image, self.trash_bin.rect)

            try: 
                if user_code_running:

                    # Draw the blocks (the drawing will now be clipped)
                    for block in block_list_1:
                        block.update(screen)

                    # Clear the clipping area after drawing the blocks
                    screen.set_clip(None)

                    screen.blit(level_surface, (0, 0))
                    if self.pixel_count == 0:
                        bot_pos = self.get_bot_position()
                        self.check_interactables(self.layout, bot_pos, screen)

                    bot_pos = self.get_bot_position()
                    self.check_interactables(self.layout, bot_pos, screen)

                    if (self.layout[self.get_bot_position()[0]][self.get_bot_position()[1]] == 3):
                        user_code_running = False
                        print("Level Complete!")
                        level_complete = True
                        
                        points = 0
                        for block in block_list_1:
                            if not block.locked:
                                points += 1
                        level_number = int(self.level)
                        if points > 1:
                            # Assuming you have a method in the User class to unlock skins
                            # and there's a method to update or check if a skin is unlocked.
                            skin_to_unlock = level_number + 1
                            self.user.unlock_skin(
                                skin_to_unlock
                            )  # Make sure you have this method or similar in your User class

                            print(f"Unlocked skin {skin_to_unlock} for user {self.user.id}.")

                        self.user.set_score(self.level, points)
                        print(f"Score updated for {self.user.id} to {points} for level 1.")
                        if level_complete:
                            self.level_complete_screen(screen)
                            return

                    if temp_block != None:
                        try:
                            if temp_block.command == "move":
                                num_moves = int(temp_block.input_box.user_text)
                                if self.pixel_count == 0 and not self.next_tile_is_open(
                                    self.layout, self.bot.direction, bot_pos
                                ):
                                    temp_block = temp_block.next
                                    continue

                                if num_moves != 0:
                                    self.bot.animate_bot()
                                    if self.bot.direction == "up":
                                        self.bot.bot_rect.y -= 1
                                    elif self.bot.direction == "down":
                                        self.bot.bot_rect.y += 1
                                    elif self.bot.direction == "left":
                                        self.bot.bot_rect.x -= 1
                                    elif self.bot.direction == "right":
                                        self.bot.bot_rect.x += 1
                                self.pixel_count += 1
                                if self.pixel_count >= tile_width:
                                    self.pixel_count = 0
                                    self.move_count += 1
                                    if (
                                        self.move_count == num_moves
                                        or not self.next_tile_is_open(
                                            self.layout, self.bot.direction, bot_pos
                                        )
                                    ):
                                        self.move_count = 0
                                        temp_block = temp_block.next

                            elif temp_block.command == "turn":
                                self.bot.turn_bot(int(temp_block.input_box.user_text))
                                temp_block = temp_block.next

                            elif temp_block.command == "if":
                                end = self.get_end_block(temp_block)
                                if temp_block.check_condition(
                                    self.layout, self.bot.direction, bot_pos, self.bot
                                ):
                                    temp_block = temp_block.next
                                else:
                                    temp_block = end.next

                            elif temp_block.command == "endif":
                                temp_block = temp_block.next

                            elif temp_block.command == "while":
                                end = self.get_end_block(temp_block)
                                if temp_block.check_condition(
                                    self.layout, self.bot.direction, bot_pos, self.bot
                                ):
                                    temp_block = temp_block.next
                                else:
                                    temp_block = end.next

                            elif temp_block.command == "endwhile":
                                temp_block = temp_block.return_to
                                
                            elif temp_block.command == "for":
                                end = self.get_end_block(temp_block)
                                if temp_block.check_condition(
                                    self.layout, self.bot.direction, bot_pos, self.bot
                                ):
                                    temp_block = temp_block.next
                                else:
                                    temp_block = end.next

                            elif temp_block.command == "endfor":
                                temp_block = temp_block.return_to

                        except IndexError:
                            temp_block = temp_block.next
                            
                        if temp_block == None:
                            user_code_running = False
                            
            except ValueError:
                show_message = True
                message_timer = pygame.time.get_ticks()
                message_text = "input error"
                user_code_running = False
            
            except Exception:
                show_message = True
                message_timer = pygame.time.get_ticks()
                message_text = "Missing End Block"
                user_code_running = False

            # draw level
            for block in block_list_1:
                if not self.scroll_rect.contains(block.obj_rect):
                    block.update(screen)

            self.obstacle_list.draw(screen)

            for button in button_list:
                button.draw(screen)

            if show_message:
                message_bg_rect = pygame.Rect(
                    0, 0, 500, 120
                )  # Background rectangle for the message
                message_bg_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
                pygame.draw.rect(
                    screen, (255, 255, 255), message_bg_rect
                )  # White background
                pygame.draw.rect(screen, (0, 0, 0), message_bg_rect, 2)  # Black border

                message_surface = font.render(message_text, True, (0, 0, 0))
                message_rect = message_surface.get_rect(
                    center=(screen.get_width() // 2, screen.get_height() // 2)
                )
                screen.blit(message_surface, message_rect)

                if pygame.time.get_ticks() - message_timer > 1500:
                    show_message = False
                    message_text = ""

            self.bot.update(screen)

            pygame.display.update()
            clock.tick(120)
                
            

# for testing just the level screen
def only_level():
    """
    A standalone function for testing the level without running the full game.
    Sets up the game environment, initializes a level, and runs it.
    
    No parameters.
    
    Returns:
        None.
    """
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("ProBot")

    level1 = Level(1, None, screen)

    level1.run_level(screen)

    pygame.quit()


#only_level()
