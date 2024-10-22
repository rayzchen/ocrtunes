def getchoice(prompt, options):
    # Take input from list of valid options
    while True:
        value = input(prompt).strip()
        if value not in options:
            print("Invalid choice!")
        else:
            return value


def format_time(time):
    if time > 3600:
        return f"{time // 3600}:{time // 60 % 60:02}:{time % 60:02}"
    else:
        return f"{time // 60 % 60}:{time % 60:02}"


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
