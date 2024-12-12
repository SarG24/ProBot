import pygame


class Button:
    """
    A button widget for Pygame applications.

    Attributes:
        image (pygame.Surface): The surface representing the button.
        rect (pygame.Rect): The rectangular area occupied by the button.
    """

    def __init__(self, position, size, color, text, font_size):
        """
        Initializes a new Button instance.

        Parameters:
            position (tuple): The (x, y) coordinates of the center of the button.
            size (tuple): The width and height of the button (width, height).
            color (tuple): The RGB color tuple representing the button's background color (R, G, B).
            text (str): The text to display on the button.
            font_size (int): The font size for the button text.
        """
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = pygame.Rect((0, 0), size)

        font = pygame.font.SysFont(None, font_size)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        self.image.blit(text, text_rect)

        # set after centering text
        self.rect.center = position

    def draw(self, screen):
        """
        Draws the button on the specified Pygame screen.

        Parameters:
            screen (pygame.Surface): The Pygame surface on which to draw the button.
        """
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        """
        Checks if the button is clicked.

        Parameters:
            event (pygame.event.Event): The Pygame event object representing the mouse event.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)

