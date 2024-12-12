import pygame
from input_box import InputBox, DropDown


class CodeBlock(pygame.sprite.Sprite):
    """
    Represents a basic code block in the game environment.

    Attributes:
        image (str): The image file path for the block.
        position (tuple): The (x, y) coordinates of the block's position.
        command (str): The command associated with the block.
        obj (pygame.Surface): The loaded image of the block.
        obj_rect (pygame.Rect): The rectangle that defines the dimensions and position of the block.
        next (CodeBlock): A reference to the next block in the sequence.
        locked (bool): Indicates whether the block is locked.
        in_sandbox (bool): Indicates whether the block is in the sandbox.
    """
    def __init__(self, image, position, command):
        """
        Initializes a new CodeBlock instance.

        Parameters:
            image (str): The image file path for the block.
            position (tuple): The (x, y) coordinates of the block's position.
            command (str): The command associated with the block.
        """
        super().__init__()

        self.image = image
        self.position = position
        self.command = command

        self.obj = pygame.image.load(image).convert_alpha()
        self.obj_rect = self.obj.get_rect(midbottom=position)

        self.next = None

        self.locked = True
        self.in_sandbox = False

    def update(self, screen):
        """
        Updates the block's appearance on the screen.

        Parameters:
            screen (pygame.Surface): The Pygame surface on which to update the block.
        """
        screen.blit(self.obj, self.obj_rect)

    def duplicate(self):
        """
        Creates a duplicate of the code block.

        Returns:
            CodeBlock: A duplicate instance of the code block.
        """
        return CodeBlock(self.image, self.position, self.command)

    def run_command(self, bot):
        """
         Runs the command associated with the block.

         Parameters:
             bot (Bot): The bot object to execute the command.
         """
        bot.bot_rect.y -= 1
        bot.move_bot()


class MoveAndTurnBlock(CodeBlock):
    """
    Represents a code block for moving and turning the bot.

    Attributes:
        input_box (InputBox): The input box for receiving user input.
    """
    def __init__(self, image, position, command):
        """
        Initializes a new MoveAndTurnBlock instance.

        Parameters:
            image (str): The image file path for the block.
            position (tuple): The (x, y) coordinates of the block's position.
            command (str): The command associated with the block.
        """
        super().__init__(image, position, command)
        self.input_box = InputBox((0, 0), (60, 20))
        self.input_box.input_rect.center = (
            self.obj_rect.centerx,
            self.obj_rect.centery + 7,
        )
        self.input_box.user_text = ""

    def update(self, screen):
        """
        Updates the appearance of the block on the screen.

        Parameters:
            screen (pygame.Surface): The Pygame surface on which to update the block.
        """
        super().update(screen)
        self.input_box.input_rect.center = (
            self.obj_rect.centerx,
            self.obj_rect.centery + 7,
        )
        self.input_box.draw(screen)

    def duplicate(self):
        """
        Creates a duplicate of the move and turn block.

        Returns:
            MoveAndTurnBlock: A duplicate instance of the move and turn block.
        """
        return MoveAndTurnBlock(self.image, self.position, self.command)


class ConditionalBlock(CodeBlock):
    """
    Represents a conditional code block in the game environment.

    Attributes:
        end (ConditionalBlock): A reference to the end block of the conditional block.
        loop_count (int): The count of loops executed by the block.
        input_box (InputBox): The input box for receiving user input.
        drop_down1 (DropDown): The drop-down menu for selecting options.
    """
    def __init__(self, image, position, command):
        """
        Initializes a new ConditionalBlock instance.

        Parameters:
            image (str): The image file path for the block.
            position (tuple): The (x, y) coordinates of the block's position.
            command (str): The command associated with the block.
        """
        super().__init__(image, position, command)

        self.end = None

        if self.command != "else":
            
            self.loop_count = 0

            self.input_box = InputBox(
                (self.obj_rect.centerx, self.obj_rect.centery + 6), (80, 17)
            )

            self.drop_down1 = DropDown(
                [(100, 80, 255), (100, 200, 255)],
                [(255, 100, 100), (255, 150, 150)],
                (self.obj_rect.centerx, self.obj_rect.centery + 6),
                (80, 17),
                "sel",
                ["wall ahead", "wall not ahead", "button is pressed", "door is open", "num", "true"],
            )

    def update(self, screen):
        """
         Updates the appearance of the block on the screen.

         Parameters:
             screen (pygame.Surface): The Pygame surface on which to update the block.
         """
        super().update(screen)

        if self.command != "else":
            if self.drop_down1.main == "num":
                self.input_box.input_rect.center = (
                    self.obj_rect.centerx,
                    self.obj_rect.centery + 6,
                )
                self.input_box.draw(screen)
            else:
                self.drop_down1.rect.center = (
                    self.obj_rect.centerx,
                    self.obj_rect.centery + 6,
                )
                self.drop_down1.draw(screen)

    def duplicate(self):
        """
        Creates a duplicate of the conditional block.

        Returns:
            ConditionalBlock: A duplicate instance of the conditional block.
        """
        return ConditionalBlock(self.image, self.position, self.command)

    def check_condition(self, layout, bot_direction, bot_pos, bot):
        """
        Checks the condition associated with the conditional block.

        Parameters:
            layout (list): The layout of the game environment.
            bot_direction (str): The direction of the bot.
            bot_pos (tuple): The position of the bot.
            bot (Bot): The bot object.

        Returns:
            bool: True if the condition is satisfied, False otherwise.
        """

        if self.drop_down1.main == "wall ahead":
            if bot_direction == "up":
                if bot.bot_rect.y == 57:
                    return True
                return layout[bot_pos[0] - 1][bot_pos[1]] == 2

            elif bot_direction == "down":
                if bot.bot_rect.y == 385:
                    return True
                return layout[bot_pos[0] + 1][bot_pos[1]] == 2

            elif bot_direction == "left":
                if bot.bot_rect.x == 60:
                    return True
                return layout[bot_pos[0]][bot_pos[1] - 1] == 2

            elif bot_direction == "right":
                if bot.bot_rect.x == 757:
                    return True
                return layout[bot_pos[0]][bot_pos[1] + 1] == 2
            
        elif self.drop_down1.main == "wall not ahead":
            if bot_direction == "up":
                if bot.bot_rect.y == 57:
                    return True
                return layout[bot_pos[0] - 1][bot_pos[1]] != 2

            elif bot_direction == "down":
                if bot.bot_rect.y == 385:
                    return True
                return layout[bot_pos[0] + 1][bot_pos[1]] != 2

            elif bot_direction == "left":
                if bot.bot_rect.x == 60:
                    return True
                return layout[bot_pos[0]][bot_pos[1] - 1] != 2

            elif bot_direction == "right":
                if bot.bot_rect.x == 757:
                    return True
                return layout[bot_pos[0]][bot_pos[1] + 1] != 2

        elif self.drop_down1.main == "button is pressed":
            pass

        elif self.drop_down1.main == "door is open":
            pass
        
        elif self.drop_down1.main == "true":
            return True
        
        else:
            if self.loop_count >= int(self.drop_down1.main):
                return False
            else:
                self.loop_count +=1
                return True


class EndConditionalBlock(CodeBlock):
    """
    Represents the end block of a conditional code block.

    Attributes:
        return_to (ConditionalBlock): A reference to the conditional block to return to.
    """
    def __init__(self, image, position, command):
        """
         Initializes a new EndConditionalBlock instance.

         Parameters:
             image (str): The image file path for the block.
             position (tuple): The (x, y) coordinates of the block's position.
             command (str): The command associated with the block.
         """
        super().__init__(image, position, command)
        self.return_to = None

    def duplicate(self):
        """
        Creates a duplicate of the end conditional block.

        Returns:
            EndConditionalBlock: A duplicate instance of the end conditional block.
        """
        return EndConditionalBlock(self.image, self.position, self.command)

