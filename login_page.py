id_list = ["yeah", "nah"]


def check_id(id):
    """
    Checks if the given ID exists in the global id_list. If it does, prints that the ID exists.
    If not, it calls create_new_user to handle the creation of a new user.

    Parameters:
        id (str): The ID to check against the id_list.
    """
    if id in id_list:
        print("id exists")
    else:
        create_new_user(id)


def create_new_user(id):
    """
    Handles the creation of a new user by printing a message indicating a new user is being created.
    This function could be expanded to include actual user creation logic.

    Parameters:
        id (str): The ID of the user to create.
    """
    print("new user")

