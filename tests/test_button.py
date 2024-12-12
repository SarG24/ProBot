import unittest
import pygame
from unittest.mock import Mock
from button import Button

class TestButton(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize pygame modules
        pygame.init()
        pygame.font.init()

    def setUp(self):
        # Setup a button instance with fixed position, size, color, text, and font size
        self.button = Button((100, 100), (50, 30), (255, 0, 0), "Click Me", 24)

    def test_is_clicked_within_bounds(self):
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN  # Use the pygame constant here
        event.button = 1
        event.pos = (110, 110)  # Position within the button's area

        self.assertTrue(self.button.is_clicked(event), "Button should detect clicks within its bounds.")

    def test_is_clicked_outside_bounds(self):
        # Create a mock event for a mouse click outside the button's bounds
        event = Mock()
        event.type = "MOUSEBUTTONDOWN"
        event.button = 1
        event.pos = (200, 200)  # Position outside the button's area

        self.assertFalse(self.button.is_clicked(event), "Button should not detect clicks outside its bounds.")

    @classmethod
    def tearDownClass(cls):
        # Uninitialize pygame modules
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
