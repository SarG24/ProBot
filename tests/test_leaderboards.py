# Import necessary modules
import unittest
from unittest.mock import Mock
from leaderboards import Leaderboard

class MockUser:
    def __init__(self, user_id, scores):
        self.id = user_id
        self.score = scores

# Define the test class
class TestLeaderboard(unittest.TestCase):

    # Set up test fixtures
    def setUp(self):
        # Create a dictionary of mock users
        self.users = {
            "user1": MockUser("user1", {1: 10, 2: 20, 3: 30}),
            "user2": MockUser("user2", {1: 15, 2: 25, 3: 5}),
            "user3": MockUser("user3", {1: 8, 2: 18, 3: 28})
        }
        self.leaderboard = Leaderboard(2, self.users)

    # Test case for getting highest score
    def test_get_highest_score(self):
        expected = "User: user2, Score: 25"
        self.assertEqual(self.leaderboard.get_highest_score(), expected)

    # Test case for getting highest overall score
    def test_get_highest_overall_score(self):
        expected = " User: user1   Score:   30   Level:   3"
        self.assertEqual(self.leaderboard.get_highest_overall_score(), expected)

    # Test case for getting lowest score
    def test_get_lowest_score(self):
        expected = "User: user3, Score: 18"
        self.assertEqual(self.leaderboard.get_lowest_score(), expected)

    # Test case for getting lowest overall score
    def test_get_lowest_overall_score(self):
        # Correct expectation based on mock data: Lowest score is 5 by user2 at level 3
        expected = " User: user2   Score:   5   Level:   3"
        self.assertEqual(self.leaderboard.get_lowest_overall_score(), expected)

    # Test case for getting average score
    def test_get_average_score(self):
        expected = 21  # Average of scores for level 2: (20 + 25 + 18) / 3
        self.assertEqual(self.leaderboard.get_average_score(), expected)

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()