# Import necessary modules
import unittest
from user import User

# Define the test class
class TestUser(unittest.TestCase):
    # Set up test fixtures
    def setUp(self):
        # Create instances of users for testing
        self.user_1 = User(1, 1)  # Regular user
        self.user_2 = User(2, 2)  # Special user

    # Test case for getting user id
    def test_get_user_id(self):
        # Check user id for regular user
        self.assertEqual(self.user_1.get_user_id(), 1)
        # Check user id for special user
        self.assertEqual(self.user_2.get_user_id(), 2)

    # Test case for getting user type
    def test_get_user_type(self):
        # Check user type for regular user
        self.assertEqual(self.user_1.get_user_type(), 1)
        # Check user type for special user
        self.assertEqual(self.user_2.get_user_type(), 2)

    # Test case for setting user score
    def test_set_score(self):
        # Set score for level 1 for regular user
        self.user_1.set_score(1, 100)
        # Check if score is set correctly
        self.assertEqual(self.user_1.get_score(1), 100)

        # Set score for level 2 for regular user
        self.user_1.set_score(2, -1)
        # Check if score is set correctly
        self.assertEqual(self.user_1.get_score(2), -1)

        # Set score for level 1 for regular user to unlock a skin
        self.user_1.set_score(1, 100)
        # Check if the next skin is unlocked
        self.assertIn(2, self.user_1.unlocked_skins)

    # Test case for getting user score
    def test_get_score(self):
        # Check score for level 1 for regular user
        self.assertEqual(self.user_1.get_score(1), 0)
        # Check score for level 2 for regular user
        self.assertEqual(self.user_1.get_score(2), -1)

    # Test case for unlocking a skin
    def test_unlock_skin(self):
        # Check if skin 2 is not initially unlocked for regular user
        self.assertNotIn(2, self.user_1.unlocked_skins)
        # Unlock skin 2 for regular user
        self.user_1.unlock_skin(2)
        # Check if skin 2 is unlocked after the operation
        self.assertIn(2, self.user_1.unlocked_skins)

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
