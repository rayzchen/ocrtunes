from ocrtunes.views import getchoice, ExitStack
from ocrtunes import account
import re


class AccountView:
    def __init__(self, ctx):
        # Store context as attr
        self.ctx = ctx

    def display(self):
        # Show menu choice
        print("You are not logged in")
        print("1) Log in")
        print("2) Sign up")
        print("3) Quit")
        choice = getchoice("Enter choice: ", ["1", "2", "3"])
        if choice == "1":
            self.login_user()
        elif choice == "2":
            self.signup_user()
        else:
            # Exit program
            raise ExitStack

    def login_user(self):
        # Prompt for name
        name = input("Enter name (leave empty to quit): ").strip()
        if not name:
            return
        user = account.login_account(self.ctx.db, name)
        if user is None:
            print("Unknown user!")
        else:
            self.ctx.login_user(user)

    def signup_user(self):
        # Validate name
        name = ""
        while True:
            name = input("Enter name (leave empty to quit): ").strip()
            if not name:
                return
            if account.login_account(self.ctx.db, name):
                print("User already exists!")
            else:
                break

        # Validate date of birth
        dob = ""
        while True:
            dob = input("Enter date of birth (DD/MM/YYYY): ").strip()
            if not re.match(
                r"^(0[1-9]|[12][0-9]|3[01])/(1[0-2]|0[1-9])/(19|20)\d\d$", dob
            ):
                print("Invalid format!")
            else:
                break
        user = account.create_account(self.ctx.db, name, dob)
        self.ctx.login_user(user)
