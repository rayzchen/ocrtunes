from ocrtunes import database
from ocrtunes.views import UserContext, ExitStack
from ocrtunes.views.account import AccountView


def viewloop():
    # Create and link database to context
    db = database.initialise_db()
    ctx = UserContext()
    ctx.set_db(db)

    # Set up views
    account_view = AccountView(ctx)

    while True:
        if not ctx.logged_in():
            account_view.display()
        else:
            print("You are logged in as", account.get_name(db, user))
            getchoice("Enter choice: ", [])


def main():
    try:
        viewloop()
    except ExitStack:
        return


if __name__ == "__main__":
    main()
