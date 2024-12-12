# Import the pygame library which is used for creating video games with Python.
import pygame

# Define a class called Leaderboard, which will handle the display of user scores for a given level.
class Leaderboard:
    # The constructor of the Leaderboard class takes two arguments:
    # level: The level number for which the leaderboard is being displayed.
    # user_dict: A dictionary of User objects which contains the user data.
    def __init__(self, level, user_dict):
        self.level = level          # Store the level number.
        self.user_dict = user_dict  # Store the dictionary of users.
        
    # Define a method to display the leaderboard on the screen.
    def display_leaderboard(self, screen):
        y_pos = 100
        # Start position for the first entry on the Y-axis.
        # Loop through each key in the user dictionary.
        for key in self.user_dict:
            if key != "admin" and key != "teacher":
                # Get the temporary user object from the dictionary.
                temp_user = self.user_dict[key]
                # Create a text surface with the user's ID and score for the current level.
                # The score is rendered in black (0, 0, 0) with a font size of 32.
                text_surface = pygame.font.SysFont(None, 32).render(f"{temp_user.id}, {temp_user.score[self.level]}", True, (255, 255, 255))
                # Draw the text surface onto the screen at the specified position (100, y_pos).
                screen.blit(text_surface, (550, y_pos))

                # Increment the y_pos by 50 pixels for the next entry, creating a vertical list.
                y_pos += 50

    def get_highest_score(self):
        highest_score = float('1')
        highest_scoring_user = None
        for user in self.user_dict.values():
            if user.id != "admin" and user.id != "teacher":
                if self.level in user.score and user.score[self.level] < highest_score:
                    highest_score = user.score[self.level]
                    highest_scoring_user = user.id
        return "User: " + str(highest_scoring_user) + ", Score: " +  str(highest_score)

    def get_highest_overall_score(self):
        highest_score = float('0')
        highest_scoring_user = None
        highest_scoring_level = None

        for user in self.user_dict.values():
            if user.id != "admin" and user.id != "teacher":
                for level in range(1, 6):
                    if level in user.score and user.score[level] < highest_score:
                        highest_score = user.score[level]
                        highest_scoring_user = user.id
                        highest_scoring_level = level

        return " User: " + str(highest_scoring_user) + "   Score:   " + str(highest_score) + "   Level:   " + str(highest_scoring_level)

    def get_lowest_score(self):
        lowest_score = float('0')
        lowest_scoring_user = None
        for user in self.user_dict.values():
            if user.id != "admin" and user.id != "teacher":
                if self.level in user.score and user.score[self.level] > lowest_score:
                    lowest_score = user.score[self.level]
                    lowest_scoring_user = user.id
        return "User: " + str(lowest_scoring_user) + ", Score: " +  str(lowest_score)

    def get_lowest_overall_score(self):
        lowest_score = float(0)
        lowest_scoring_user = None
        lowest_scoring_level = None

        for user in self.user_dict.values():
            if user.id != "admin" and user.id != "teacher":
                for level in range(1, 6):
                    if level in user.score and user.score[level]>lowest_score:
                        lowest_score = user.score[level]
                        lowest_scoring_user = user.id
                        lowest_scoring_level = level

        return " User: " + str(lowest_scoring_user) + "   Score:   " + str(lowest_score) + "   Level:   " + str(lowest_scoring_level)

    def get_average_score(self):
        total_score = 0
        num_of_users = 0

        for user in self.user_dict.values():
            if user.id != "admin" and user.id != "teacher":
                if self.level in user.score:
                    total_score += user.score[self.level]
                    num_of_users += 1

        if num_of_users > 0:
            average_score = total_score / num_of_users
            return average_score
        else:
            return None

    def get_average_overall_score(self):
        for level in range(1, 6):
            average_score = 0
            total_score = 0
            num_of_users = 0

            for user in self.user_dict.values():
                if user.id != "admin" and user.id != "teacher":
                    if level in user.score:
                        total_score += user.score[level]
                        num_of_users += 1

            if num_of_users > 0:
                average_score = total_score / num_of_users

        return average_score