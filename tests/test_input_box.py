import unittest
from unittest.mock import Mock, patch
import pygame
import os

from input_box import InputBox

class TestInputBox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.display.init()

    def setUp(self):
        pygame.font.init()
        self.mock_font = Mock()
        self.mock_font.render = Mock(return_value=pygame.Surface((100, 50)))
        self.input_box = InputBox((150, 100), (200, 50))
        self.input_box.base_font = self.mock_font

    def test_input_box_initialization(self):
        self.assertEqual(self.input_box.user_text, "")
        self.assertTrue(self.input_box.active)

    def test_take_input_keydown(self):
        # Simulate typing the character 'a'
        event_char = pygame.event.Event(pygame.KEYDOWN, unicode='a', key=pygame.K_a)
        self.input_box.take_input(event_char)
        self.assertEqual(self.input_box.user_text, 'a', "The input box should contain 'a' after typing 'a'.")

        # Now simulate backspace press to remove 'a'
        event_backspace = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
        self.input_box.take_input(event_backspace)
        self.assertEqual(self.input_box.user_text, '', "The input box should be empty after pressing backspace.")


    def test_draw(self):
        # Directly testing draw method without trying to mock blit
        mock_screen = pygame.Surface((800, 600))
        try:
            self.input_box.draw(mock_screen)
            test_passed = True
        except Exception as e:
            test_passed = False
        self.assertTrue(test_passed)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        del os.environ['SDL_VIDEODRIVER']

if __name__ == '__main__':
    unittest.main()
