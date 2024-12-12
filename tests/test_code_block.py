import unittest
from unittest.mock import Mock, patch
import pygame
import os

from code_block import CodeBlock, MoveAndTurnBlock, ConditionalBlock, EndConditionalBlock


class TestCodeBlocks(unittest.TestCase):

    def setUp(self):
        # Set the environment variable to use a "dummy" video driver.
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        # Initialize pygame modules necessary for tests.
        pygame.init()
        pygame.font.init()

        # Mocking pygame modules that require a display mode
        self.mock_screen = Mock()
        self.mock_screen.blit = Mock()

        # Mock the image and Surface methods from pygame
        self.mock_image = Mock()
        self.mock_image.convert_alpha = Mock(return_value=pygame.Surface((1, 1)))
        pygame.image.load = Mock(return_value=self.mock_image)
        
        self.code_block_image = 'block.png'
        self.position = (100, 100)
        self.command = 'forward'
        
        self.bot_mock = Mock()
        self.bot_mock.bot_rect = pygame.Rect(0, 0, 50, 50)
        self.bot_mock.move_bot = Mock()

    def test_code_block_initialization(self):
        block = CodeBlock(self.code_block_image, self.position, self.command)
        self.assertEqual(block.position, self.position)
        self.assertEqual(block.command, self.command)

    def test_code_block_duplicate(self):
        block = CodeBlock(self.code_block_image, self.position, self.command)
        duplicate_block = block.duplicate()
        self.assertIsInstance(duplicate_block, CodeBlock)
        self.assertNotEqual(id(block), id(duplicate_block))

    def test_code_block_run_command(self):
        block = CodeBlock(self.code_block_image, self.position, self.command)
        block.run_command(self.bot_mock)
        self.bot_mock.move_bot.assert_called_once()

    def test_move_and_turn_block_initialization(self):
        block = MoveAndTurnBlock(self.code_block_image, self.position, self.command)
        self.assertEqual(block.position, self.position)
        self.assertEqual(block.command, self.command)
        self.assertIsNotNone(block.input_box)

    def test_move_and_turn_block_duplicate(self):
        block = MoveAndTurnBlock(self.code_block_image, self.position, self.command)
        duplicate_block = block.duplicate()
        self.assertIsInstance(duplicate_block, MoveAndTurnBlock)

    def test_conditional_block_initialization(self):
        block = ConditionalBlock(self.code_block_image, self.position, 'if')
        self.assertEqual(block.position, self.position)
        self.assertEqual(block.command, 'if')

    def test_conditional_block_check_condition_true(self):
        block = ConditionalBlock(self.code_block_image, self.position, 'if')
        block.drop_down1 = Mock()
        block.drop_down1.main = 'true'
        result = block.check_condition([], 'up', (0, 0), self.bot_mock)
        self.assertTrue(result)

    def test_end_conditional_block_initialization(self):
        block = EndConditionalBlock(self.code_block_image, self.position, 'end')
        self.assertEqual(block.position, self.position)
        self.assertEqual(block.command, 'end')

    def test_end_conditional_block_duplicate(self):
        block = EndConditionalBlock(self.code_block_image, self.position, 'end')
        duplicate_block = block.duplicate()
        self.assertIsInstance(duplicate_block, EndConditionalBlock)

    # Add teardown to quit pygame and clean up environment variables
    def tearDown(self):
        pygame.quit()
        del os.environ['SDL_VIDEODRIVER']

if __name__ == '__main__':
    unittest.main()

