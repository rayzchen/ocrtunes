def getchoice(prompt, options):
    # Take input from list of valid options
    while True:
        value = input(prompt).strip()
        if value not in options:
            print("Invalid choice!")
        else:
            return value


class UserContext:
    def __init__(self):
        # Initialise attributes shared between views
        self.user = None
        self.db = None

    def login_user(self, user):
        self.user = user

    def set_db(self, db):
        self.db = db

    def logged_in(self):
        return self.user is not None

    def logout(self):
        self.user = None


class ExitStack(Exception):
    pass
