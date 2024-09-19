import database
import account
import re

user = None
db = None

class ExitStack(Exception):
    pass

def getchoice(prompt, options):
    while True:
        value = input(prompt).strip()
        if value not in options:
            print("Invalid choice!")
        else:
            return value

def login_menu():
    print("You are not logged in")
    print("1) Log in")
    print("2) Sign up")
    print("3) Quit")
    choice = getchoice("Enter choice: ", ["1", "2", "3"])
    if choice == "1":
        login_user()
    elif choice == "2":
        signup_user()
    else:
        raise ExitStack

def login_user():
    global user
    name = input("Enter name (leave empty to quit): ").strip()
    if not name:
        return
    user = account.login_account(db, name)
    if user is None:
        print("Unknown user!")

def signup_user():
    global user
    name = ""
    while True:
        name = input("Enter name (leave empty to quit): ").strip()
        print(name)
        if not name:
            return
        if account.login_account(db, user):
            print("User already exists!")
        else:
            break
    dob = ""
    while True:
        dob = input("Enter date of birth (DD/MM/YYYY): ").strip()
        if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(1[0-2]|0[1-9])/(19|20)\d\d$", dob):
            print("Invalid format!")
        else:
            break
    user = account.create_account(db, name, dob)
    print(user)

def main():
    global db
    db = database.initialise_db()
    while True:
        try:
            if user is None:
                login_menu()
            else:
                print("You are logged in as", account.get_name(db, user))
                getchoice("Enter choice: ", [])
        except ExitStack:
            break

if __name__ == "__main__":
    main()
