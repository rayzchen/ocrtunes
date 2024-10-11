from ocrtunes.views import getchoice, ExitStack
from ocrtunes import account


class ProfileView:
    def __init__(self, ctx):
        # Store context as attr
        self.ctx = ctx

    def display(self):
        # Show menu choice
        username = account.get_name(self.ctx.db, self.ctx.user)
        print("You are logged in as", username)

        print("1) View profile")
        print("2) Log out")
        choice = getchoice("Enter choice: ", ["1", "2"])
        if choice == "1":
            self.view_profile()
        elif choice == "2":
            self.ctx.logout()

    def view_profile(self):
        # Display profile
        fav_artist = account.get_fav_artist(self.ctx.db, self.ctx.user)
        fav_genre = account.get_fav_genre(self.ctx.db, self.ctx.user)
        print("Favourite artist: ", fav_artist)
        print("Favourite genre: ", fav_genre)

        # Show menu choice
        print("1) Edit favourite artist")
        print("2) Edit favourite genre")
        print("3) Quit")
        choice = getchoice("Enter choice: ", ["1", "2", "3"])
        if choice == "1":
            self.edit_fav_artist()
        elif choice == "2":
            self.edit_fav_genre()
        else:
            return

    def edit_fav_artist(self):
        current_artist = account.get_fav_artist(self.ctx.db, self.ctx.user)
        print("Current favourite artist:", current_artist)
        new_artist = input("Enter favourite artist (leave blank to reset): ")
        if not new_artist:
            new_artist = "None"
        account.set_fav_artist(self.ctx.db, self.ctx.user, new_artist)
        print("Successfully set favourite artist to", new_artist)

    def edit_fav_genre(self):
        current_genre = account.get_fav_genre(self.ctx.db, self.ctx.user)
        print("Current favourite genre:", current_genre)
        new_genre = input("Enter favourite genre (leave blank to reset): ")
        if not new_genre:
            new_genre = "None"
        account.set_fav_genre(self.ctx.db, self.ctx.user, new_genre)
        print("Successfully set favourite genre to", new_genre)
