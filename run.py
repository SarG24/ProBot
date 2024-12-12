import pygame
import pickle
import pathlib
from levels import Level, Tutorial
from button import Button
from input_box import InputBox
from user import User
from leaderboards import Leaderboard
from pathlib import Path

# the base dictionary of users (admin and teacher will have special privalages)
user_dict = {"admin": User("admin", 2), "teacher": User("teacher", 2)}

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

images = Path("images")

def login(screen):

    """
    Handles the login process for the game.

    Displays the login screen where users can enter their ID. New users are added to the user_dict.
    After successful login, the user is taken to the main menu.

    Args:
        screen (pygame.Surface): The main screen surface where the login UI is drawn.
    """

    running = True

    # creates the clock so the game can run at 60fps
    clock = pygame.time.Clock()

    # create buttons
    start_button = Button((600, 350), (100, 50), "blue", "Enter", 32)
    exit_button = Button((50, 575), (100, 50), "blue", "Exit", 32)

    input_box = InputBox((600, 250), (450, 50))

    while running:
        # loop that checks if any events happen, like clicking or button presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if exit_button.is_clicked(event):
                return
            if input_box.take_input(event) or start_button.is_clicked(event):
                id = input_box.user_text
                if id in user_dict.keys():
                    print("id exists")
                    main_menu(screen, user_dict[id])

                else:
                    print("new user")
                    new_user = User(id, 0)
                    user_dict[id] = new_user
                    main_menu(screen, new_user)

        screen.fill("white")
        start_button.draw(screen)
        exit_button.draw(screen)

        input_box.draw(screen)

        pygame.display.update()
        clock.tick(120)


def main_menu(screen, user):

    """
    Displays the main menu of the game.

    From the main menu, users can start the game, view the leaderboard, select skins,
    or access the instructor dashboard if they have the required privileges.

    Args:
        screen (pygame.Surface): The main screen surface where the main menu UI is drawn.
        user (User): The currently logged-in user.
    """

    # save user info
    save_game()

    running = True
    clock = pygame.time.Clock()

    start_button = Button((300, 200), (150, 50), "blue", "Start Game", 32)
    exit_button = Button((50, 575), (100, 50), "blue", "Exit", 32)
    leaderboard_button = Button((300, 300), (150, 50), "blue", "Leaderboard", 32)
    select_skin_button = Button((300, 400), (150, 50), "blue", "Select Skin", 32)
    instructor_dashboard_button = Button((300, 500), (190, 50), "blue", "Instructor Dashboard", 26)

    # Load the skin image based on the user's choice or default to ProBot-1 if not set
    skin_image_path = getattr(user, "skin", "ProBot-1.png")
    bot = pygame.image.load(images / "robot" / skin_image_path).convert_alpha()
    bot = pygame.transform.smoothscale(bot, (416, 416))
    bot_rect = bot.get_rect(center=(800, 300))

    text = pygame.font.SysFont(None, 32).render(user.id, True, (0, 0, 0))

    credit_font = pygame.font.SysFont(None, 24)
    credit_text = credit_font.render(
        "Developed by Team 35. CS2212B, Winter 2024.", True, (0, 0, 0)
    )
    credit_textTwo = credit_font.render(
        "Hani Al Gherwi, Patrick De Sousa, Shubh Patel, Sartaj Grewal, Zarif Tajwar Ahmed.",
        True,
        (0, 0, 0),
    )
    credit_text_rect = credit_text.get_rect(
        center=(600, 550)
    )  # Position might need to be adjusted
    credit_text_rectTwo = credit_textTwo.get_rect(
        center=(600, credit_text_rect.bottom + 20)
    )  # Added 20 pixels for spacing

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_button.is_clicked(event):
                running = False
                pygame.quit()
                exit()
            if start_button.is_clicked(event):
                level_select(screen, user)
            if leaderboard_button.is_clicked(event):
                leaderboard(screen, user)
            if select_skin_button.is_clicked(event):
                select_skin(screen, user)
            if instructor_dashboard_button.is_clicked(event):
                if user.type == 2:
                    instructor_dashboard(screen, user)
                    # Reload the skin after potentially changing it
                    skin_image_path = user.skin if user.skin else "ProBot-1.png"
                    bot = pygame.image.load(
                        images / "robot" / skin_image_path
                    ).convert_alpha()
                    bot = pygame.transform.smoothscale(bot, (416, 416))
                    bot_rect = bot.get_rect(center=(800, 300))

        screen.fill((255, 229, 153))
        screen.blit(bot, bot_rect)
        screen.blit(text, ((800 - (text.get_width() / 2)), 50))
        screen.blit(credit_text, credit_text_rect)
        screen.blit(credit_textTwo, credit_text_rectTwo)

        start_button.draw(screen)
        leaderboard_button.draw(screen)
        select_skin_button.draw(screen)
        exit_button.draw(screen)
        if user.type == 2:
            instructor_dashboard_button.draw(screen)

        pygame.display.update()
        clock.tick(120)


def level_select(screen, user):

    """
    Displays the level selection screen.

    Users can choose from available levels including tutorial and levels 1-5. 
    Selecting a level initiates the level gameplay.

    Args:
        screen (pygame.Surface): The main screen surface where the level selection UI is drawn.
        user (User): The currently logged-in user.
    """

    running = True

    back_button = Button((50, 575), (100, 50), "Red", "Back", 50)
    button1 = Button((100, 300), (200, 100), "white", "Tutorial", 60)
    button2 = Button((300, 300), (75, 100), "white", "1", 60)
    button3 = Button((500, 300), (75, 100), "white", "2", 60)
    button4 = Button((700, 300), (75, 100), "white", "3", 60)
    button5 = Button((900, 300), (75, 100), "white", "4", 60)
    button6 = Button((1100, 300), (75, 100), "white", "5", 60)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if back_button.is_clicked(event):
                return
            if button1.is_clicked(event):  # Assuming this is the tutorial button
                tutorial_level = Level(
                    "tutorial", user, screen, "This is where future hints will be!"
                )  # Pass the screen here
                tutorial = Tutorial(screen)
                tutorial.run()
                action = tutorial_level.run_level(
                    screen
                )  # Now call run_level after the tutorial.run() ends
                if action == "main_menu":
                    return
            elif button2.is_clicked(event):
                level_one = Level("1", user, screen, "Just use turn and move...")
                action = level_one.run_level(screen)
                save_game()
                if action == "main_menu":
                    return
            elif button3.is_clicked(event):
                level_two = Level("2", user, screen, "Level 1... But longer!")
                action = level_two.run_level(screen)
                save_game()
                if action == "main_menu":
                    return
            elif button4.is_clicked(event):
                level_three = Level("3", user, screen, "Just use one loop (make sure to check for walls!)")
                action = level_three.run_level(screen)
                save_game()
                if action == "main_menu":
                    return
            elif button5.is_clicked(event):
                level_two = Level("4", user, screen, "Use a while loop!")
                action = level_two.run_level(screen)
                save_game()
                if action == "main_menu":
                    return
            elif button6.is_clicked(event):
                level_three = Level("5", user, screen, "Find the right button using loops!")
                action = level_three.run_level(screen)
                save_game()
                if action == "main_menu":
                    return

        background_image = pygame.image.load("images/menus/background.jpg").convert()
        background_image = pygame.transform.scale(
            background_image, (1200, 600)
        )  # Resize to match your screen
        screen.blit(background_image, (0, 0))
        back_button.draw(screen)
        button1.draw(screen)
        button2.draw(screen)
        button3.draw(screen)
        button4.draw(screen)
        button5.draw(screen)
        button6.draw(screen)

        pygame.display.update()
        clock.tick(120)


def leaderboard(screen, user):

    """
    Displays the leaderboard for the game.

    Shows the highest scores across all users for each level. Users can navigate back to the main menu.

    Args:
        screen (pygame.Surface): The main screen surface where the leaderboard UI is drawn.
        user (User): The currently logged-in user who is viewing the leaderboard.
    """


    running = True
    clock = pygame.time.Clock()

    background_image = pygame.image.load("images/menus/background.jpg").convert()
    background_image = pygame.transform.scale(
        background_image, (1200, 600)
    )  # Resize to match your screen
    screen.blit(background_image, (0, 0))
    board1 = Leaderboard(1, user_dict)
    board2 = Leaderboard(2, user_dict)
    board3 = Leaderboard(3, user_dict)
    board4 = Leaderboard(4, user_dict)
    board5 = Leaderboard(5, user_dict)

    exit_button = Button((50, 575), (125, 55), "Red", "Exit", 55)
    level1_button = Button((200, 50), (125, 50), "white", "Level 1", 40)
    level2_button = Button((400, 50), (125, 50), "white", "Level 2", 40)
    level3_button = Button((600, 50), (125, 50), "white", "Level 3", 40)
    level4_button = Button((800, 50), (125, 50), "white", "Level 4", 40)
    level5_button = Button((1000, 50), (125, 50), "white", "Level 5", 40)

    board1.display_leaderboard(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if exit_button.is_clicked(event):
                return
            if level1_button.is_clicked(event):
                screen.blit(background_image, (0, 0))
                board1.display_leaderboard(screen)
            if level2_button.is_clicked(event):
                screen.blit(background_image, (0, 0))
                board2.display_leaderboard(screen)
            if level3_button.is_clicked(event):
                screen.blit(background_image, (0, 0))
                board3.display_leaderboard(screen)
            if level4_button.is_clicked(event):
                screen.blit(background_image, (0, 0))
                board4.display_leaderboard(screen)
            if level5_button.is_clicked(event):
                screen.blit(background_image, (0, 0))
                board5.display_leaderboard(screen)

        exit_button.draw(screen)
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)
        level4_button.draw(screen)
        level5_button.draw(screen)

        pygame.display.update()
        clock.tick(120)


def select_skin(screen, user):

    """
    Allows users to select a skin for their character in the game.

    Displays available skins and lets the user choose one. Skins can be locked or unlocked based on
    the user's progress. The selected skin is saved to the user's profile.

    Args:
        screen (pygame.Surface): The main screen surface where skin selection UI is drawn.
        user (User): The user who is selecting a skin.
    """

    running = True
    clock = pygame.time.Clock()

    button_size = (150, 75)
    button_positions = [
        (100, 275),
        (450, 275),
        (800, 275),
        (100, 450),
        (450, 450),
        (800, 450),
    ]
    skin_buttons = [
        Button(pos, button_size, "white", f"Skin {i+1}", 32)
        for i, pos in enumerate(button_positions)
    ]
    image_positions = [
        (pos[0] + button_size[0] // 2, pos[1] - 75) for pos in button_positions
    ]
    skin_images = [
        pygame.transform.smoothscale(
            pygame.image.load(f"images/robot/ProBot-{i+1}.png").convert_alpha(),
            (100, 100),
        )
        for i in range(6)
    ]
    back_button = Button((50, 575), (100, 50), "blue", "Back", 32)

    font = pygame.font.SysFont(None, 30)
    show_locked_message = False
    locked_message_timer = 0
    locked_message_text = ""  # To hold the custom message

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if back_button.is_clicked(event):
                return
            for i, button in enumerate(skin_buttons):
                if button.is_clicked(event):
                    if (i + 1) in user.unlocked_skins:
                        user.skin = f"ProBot-{i+1}.png"
                        main_menu(screen, user)  # Return to main menu only if the skin is unlocked
                        return  # This is important to exit the function after transition
                    else:
                        show_locked_message = True
                        locked_message_timer = pygame.time.get_ticks()
                        locked_message_text = (
                            f"Skin {i+1} is locked. Complete Level {i} to unlock."
                        )

        screen.fill((255, 229, 153))

        for i, button in enumerate(skin_buttons):
            button.draw(screen)
            image_rect = skin_images[i].get_rect(center=image_positions[i])
            screen.blit(skin_images[i], image_rect.topleft)

        if show_locked_message:
            message_bg_rect = pygame.Rect(
                0, 0, 500, 120
            )  # Background rectangle for the message
            message_bg_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            pygame.draw.rect(
                screen, (255, 255, 255), message_bg_rect
            )  # White background
            pygame.draw.rect(screen, (0, 0, 0), message_bg_rect, 2)  # Black border

            message_surface = font.render(locked_message_text, True, (0, 0, 0))
            message_rect = message_surface.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )
            screen.blit(message_surface, message_rect)

            if pygame.time.get_ticks() - locked_message_timer > 1500:
                show_locked_message = False
                locked_message_text = ""

        back_button.draw(screen)
        pygame.display.update()
        clock.tick(60)


def instructor_dashboard(screen, user):

    """
    Opens an instructor dashboard interface allowing selection of different levels and displays leaderboard information.

    Args:
        screen (pygame.Surface): The surface object representing the game window.
        user (str): The username of the instructor.

    Returns:
        None
    """
    running = True
    clock = pygame.time.Clock()

    # Explicitly create level selection buttons
    level1_button = Button((200, 50), (125, 50), "white", "Level 1", 40)
    level2_button = Button((400, 50), (125, 50), "white", "Level 2", 40)
    level3_button = Button((600, 50), (125, 50), "white", "Level 3", 40)
    level4_button = Button((800, 50), (125, 50), "white", "Level 4", 40)
    level5_button = Button((1000, 50), (125, 50), "white", "Level 5", 40)
    back_button = Button((50, 575), (100, 50), "blue", "Back", 32)

    # Default level of interest
    current_level = 1
    leaderboard = Leaderboard(current_level, user_dict)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if back_button.is_clicked(event):
                return

            # Check which level button is clicked
            if level1_button.is_clicked(event):
                current_level = 1
            elif level2_button.is_clicked(event):
                current_level = 2
            elif level3_button.is_clicked(event):
                current_level = 3
            elif level4_button.is_clicked(event):
                current_level = 4
            elif level5_button.is_clicked(event):
                current_level = 5

        screen.fill((255, 229, 153))  # Fill screen with a background color

        # Update and display the leaderboard for the current level
        leaderboard = Leaderboard(current_level, user_dict)
        highest_score = leaderboard.get_highest_score()
        lowest_score = leaderboard.get_lowest_score()
        average_score = leaderboard.get_average_score()
        highest_overall_score = leaderboard.get_highest_overall_score()
        lowest_overall_score = leaderboard.get_lowest_overall_score()
        overall_average_score = leaderboard.get_average_overall_score()
        font = pygame.font.SysFont(None, 32)
        if highest_score is not None:
            highest_score_text = font.render(f"Level {current_level} - Highest Score: {highest_score}", True, (0, 0, 0))
            screen.blit(highest_score_text, (50, 100))
        if lowest_score is not None:
            lowest_score_text = font.render(f"Level {current_level} - Lowest Score: {lowest_score}", True, (0, 0, 0))
            screen.blit(lowest_score_text, (50, 150))
        if average_score is not None:
            average_score_text = font.render(f"Level {current_level} - Average Score: {average_score}", True, (0, 0, 0))
            screen.blit(average_score_text, (50, 200))
        if highest_overall_score is not None:
            highest_overall_score_text = font.render(f"Highest Overall Score: {highest_overall_score}", True, (0, 0, 0))
            screen.blit(highest_overall_score_text, (50, 350))
        if lowest_overall_score is not None:
            lowest_overall_score_text = font.render(f"Lowest Overall Score: {lowest_overall_score}", True, (0, 0, 0))
            screen.blit(lowest_overall_score_text, (50, 400))
        if overall_average_score is not None:
            overall_average_score_text = font.render(f"Overall Average Score: {overall_average_score}", True, (0, 0, 0))
            screen.blit(overall_average_score_text, (50, 450))

        # Draw the level selection and back buttons
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)
        level4_button.draw(screen)
        level5_button.draw(screen)
        back_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

# resets the saved game data
def reset_data():
    """
    Resets the saved game data by overwriting the user_dict pickle file.

    Returns:
        None
    """
    with open("user_dict.pickle", "wb") as handle:
        pickle.dump(user_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def save_game():
    with open("user_dict.pickle", "wb") as handle:
        pickle.dump(user_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# pygame set up
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("ProBot")

#reset_data()

# loads saved game data
with open("user_dict.pickle", "rb") as handle:
    user_dict = pickle.load(handle)

login(screen)


pygame.quit()
