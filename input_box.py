# Import the pygame library which is used for creating video games with Python.
import pygame

# Define a class called InputBox, which will handle the creation and interaction of a text input field.
class InputBox:
    """
    A class representing a text input box in a pygame application.

    Attributes:
        size (tuple): A tuple containing the width and height of the input box.
        base_font (pygame.font.Font): The font object used for rendering text.
        user_text (str): The text entered by the user.
        input_rect (pygame.Rect): A rectangular area representing the input box.
        active (bool): Indicates whether the input box is currently active for text entry.

    Methods:
        __init__(pos, size):
            Initialize the InputBox instance.

        take_input(event):
            Handle events for the input box, such as text entry and focusing.

        draw(screen):
            Draw the input box and entered text on the screen.
    """
    # Constructor of the InputBox class.
    # pos: A tuple containing the (x, y) position of the input box.
    # size: A tuple containing the (width, height) of the input box.
    def __init__(self, pos, size):
        """
        Initialize the InputBox instance.

        Args:
            pos (tuple): The (x, y) position of the input box.
            size (tuple): The (width, height) of the input box.
        """
        self.size = size  # Store the size of the input box.
        # Initialize the font object with the default system font and the specified font size.
        self.base_font = pygame.font.Font(None, size[1])
        self.user_text = ""  # A string to store the text entered by the user.
        # Create a Rect object which helps in positioning the input box on the screen.
        self.input_rect = pygame.Rect(pos, size)
        # Render the initial text surface with the empty user_text.
        self.text_surface = self.base_font.render(self.user_text, True, (0, 0, 0))

        # Center the input box at the specified position.
        self.input_rect.center = pos

        # A boolean to keep track if the input box is currently active (i.e., ready to take input).
        self.active = True

    # A method to handle events for the input box, such as text entry and focusing.
    def take_input(self, event):
        """
        Handle events for the input box.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if the user has finished typing (Enter/Return key pressed), False otherwise.
        """
        # Check for a mouse button down event.
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the input box is clicked, activate it.
            if self.input_rect.collidepoint(event.pos):
                self.active = True
            # If somewhere else is clicked, deactivate the input box.
            else:
                self.active = False
        # Check for key down events.
        if event.type == pygame.KEYDOWN:
            # If the input box is active, take input.
            if self.active:
                # If Return/Enter key is pressed, indicate that the user has finished typing.
                if event.key == pygame.K_RETURN:
                    return True
                # If the backspace key is pressed, remove the last character from the user_text.
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[0:-1]
                # Otherwise, add the pressed key to the user_text.
                else:
                    self.user_text += event.unicode
                # Update the text surface with the current user_text.
                self.text_surface = self.base_font.render(self.user_text, True, (0, 0, 0))

    # A method to draw the input box and the entered text on the screen.
    def draw(self, screen):
        """
        Draw the input box and entered text on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        # Adjust the width of the input box if the text is wider than the box.
        self.input_rect.w = max(self.size[0], self.text_surface.get_width() + (self.size[1]/2))
        # Blit the text surface to the screen at the position of the input box.
        screen.blit(self.text_surface, (self.input_rect.x + (self.size[1]/5), self.input_rect.y + (self.size[1]/5)))
        # Re-render the text surface to ensure the latest text is displayed.
        self.text_surface = self.base_font.render(self.user_text, True, (0, 0, 0))
        # Draw a blue border around the input box.
        pygame.draw.rect(screen, "blue", self.input_rect, 2)


class DropDown:
    """
    A class representing a dropdown menu in a pygame application.

    Attributes:
        color_menu (tuple): Color tuple for the menu.
        color_option (tuple): Color tuple for the options.
        rect (pygame.Rect): Rectangular area representing the dropdown.
        font (pygame.font.Font): Font object used for rendering text.
        main (str): The currently selected option.
        options (list): List of available options.
        draw_menu (bool): Indicates whether to draw the dropdown menu.
        menu_active (bool): Indicates whether the menu is active.
        active_option (int): Index of the currently active option.

    Methods:
        __init__(color_menu, color_option, pos, size, main, options):
            Initialize the DropDown instance.

        draw(surf):
            Draw the dropdown menu.

        update(event):
            Update the dropdown menu based on events.

    """
    def __init__(self, color_menu, color_option, pos, size, main, options):
        """
        Initialize the DropDown instance.

        Args:
            color_menu (tuple): Color tuple for the menu.
            color_option (tuple): Color tuple for the options.
            pos (tuple): The (x, y) position of the dropdown.
            size (tuple): The (width, height) of the dropdown.
            main (str): The initially selected option.
            options (list): List of available options.
        """
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, size[1])
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        
    def draw(self, surf):
        """
         Draw the dropdown menu.

         Args:
             surf (pygame.Surface): The surface to draw on.
         """
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
                
    def update(self, event):
        """
        Update the dropdown menu based on events.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            int: The index of the selected option, or -1 if no option selected.
        """
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                return self.active_option
                
        return -1

