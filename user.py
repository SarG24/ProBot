class User:
    """
       Represents a user with attributes for identification, user type, score, and skin customization.

       Attributes:
           id (int): Unique identifier for the user.
           type (int): Type of the user, where type 2 represents a premium user.
           score (dict): A dictionary mapping level numbers to scores.
           skin (str): The file name of the current skin used by the user. Default is "ProBot-1.png".
           unlocked_skins (list): List of skin numbers that the user has unlocked. Premium users start with six skins unlocked.
       """
    def __init__(self, id, type, skin="ProBot-1.png"):
        """
                Initializes a new User instance with a unique ID, user type, and optionally a skin file name.

                Parameters:
                    id (int): The unique identifier for the user.
                    type (int): The type of the user (e.g., premium users are type 2).
                    skin (str): The skin file name to use for the user. Defaults to "ProBot-1.png".
                """
        self.id = id
        self.type = type
        self.score = {1: 100, 2: 100, 3: 100, 4: 100, 5: 100}
        self.skin = skin
        
        if type == 2:
            self.unlocked_skins = [1, 2, 3, 4, 5, 6]
        else:
            self.unlocked_skins = [1]
        
    def get_user_id(self):
        """
                Retrieves the user's ID.

                Returns:
                    int: The user's unique identifier.
                """
        return self.id

    def get_user_type(self):
        """
                Retrieves the user's type.

                Returns:
                    int: The user's type. For example, 2 represents a premium user.
                """
        return self.type

    def set_score(self, level, score):
        """
                Sets the score for a specified level. Unlocks a new skin if the score is positive and the next level's skin isn't already unlocked.

                Parameters:
                    level (int): The level number for which to set the score.
                    score (int): The score to set for the specified level.
                """
        self.score[int(level)] = score
        if score < 100 and (int(level) + 1) not in self.unlocked_skins:
            self.unlock_skin(int(level) + 1)

    def get_score(self, level):
        """
                Retrieves the score for a specified level.

                Parameters:
                    level (int): The level number for which to retrieve the score.

                Returns:
                    int: The score for the specified level.
                """
        return self.score[int(level)]

    def unlock_skin(self, skin_number):
        """
               Unlocks a new skin for the user.

               Parameters:
                   skin_number (int): The number of the skin to unlock.
               """
        self.unlocked_skins.append(skin_number)
