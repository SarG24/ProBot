# Import necessary modules
import unittest
from unittest.mock import patch, MagicMock
import pygame
import os
from levels import Level  # Adjust import according to your project structure

# Define the test class
class TestLevel(unittest.TestCase):
    # Set up class fixtures
    @classmethod
    def setUpClass(cls):
        # Set up a headless display driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.font.init()
        # Since we're using a dummy video driver, we can safely set a display mode.
        pygame.display.set_mode((1, 1))

    # Set up test fixtures
    def setUp(self):
        # Mock screen for pygame display
        self.mock_screen = pygame.Surface((800, 600))
        # Mock user for passing into Level instances
        self.mock_user = MagicMock()
        # Instance of the Level class to test
        self.level = Level('1', self.mock_user, self.mock_screen)

    # Test case for initializing level
    def test_level_init(self):
        """Test if the level is initialized correctly."""
        self.assertEqual(self.level.level, '1', "Level number should be initialized correctly.")

    # Test case for getting user code
    @patch('levels.Level.get_user_code', return_value=None)
    def test_get_user_code(self, mocked_get_user_code):
        """Test the get_user_code method."""
        self.level.get_user_code()
        mocked_get_user_code.assert_called_once()

    # Test case for getting end block
    @patch('levels.Level.get_end_block', return_value=None)
    def test_get_end_block(self, mocked_get_end_block):
        """Test the get_end_block method."""
        block = MagicMock()
        self.level.get_end_block(block)
        mocked_get_end_block.assert_called_once_with(block)

    # Test case for getting bot position
    @patch('levels.Level.get_bot_position', return_value=(0, 0))
    def test_get_bot_position(self, mocked_get_bot_position):
        """Test the get_bot_position method."""
        position = self.level.get_bot_position()
        mocked_get_bot_position.assert_called_once()
        self.assertEqual(position, (0, 0), "Bot position should be returned correctly.")

    # Test case for checking if next tile is open
    @patch('levels.Level.next_tile_is_open', return_value=True)
    def test_next_tile_is_open(self, mocked_next_tile_is_open):
        """Test the next_tile_is_open method."""
        result = self.level.next_tile_is_open(self.level.layout, 'up', (0, 0))
        mocked_next_tile_is_open.assert_called_once()
        self.assertTrue(result, "Next tile should be reported as open.")

    # Test case for checking interactables
    @patch('levels.Level.check_interactables', return_value=None)
    def test_check_interactables(self, mocked_check_interactables):
        """Test the check_interactables method."""
        self.level.check_interactables(self.level.layout, (0, 0), self.mock_screen)
        mocked_check_interactables.assert_called_once()

    # Test case for running level
    @patch('levels.Level.run_level', return_value=None)
    def test_run_level(self, mocked_run_level):
        """Test the run_level method."""
        self.level.run_level(self.mock_screen)
        mocked_run_level.assert_called_once()

    # Tear down class fixtures
    @classmethod
    def tearDownClass(cls):
        pygame.quit()

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
