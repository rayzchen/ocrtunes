from ocrtunes import database
from ocrtunes.views import UserContext, ExitStack
from ocrtunes.views.account import AccountView
from ocrtunes.views.profile import ProfileView
from ocrtunes.views.playlist import PlaylistView
from ocrtunes.views.songs import SongsView
import textwrap


def viewloop():
    # Create and link database to context
    db = database.initialise_db()
    ctx = UserContext()
    ctx.set_db(db)

    # Set up views
    account_view = AccountView(ctx)
    profile_view = ProfileView(ctx)
    playlist_view = PlaylistView(ctx)
    songs_view = SongsView(ctx)
    profile_view.set_playlist_view(playlist_view)
    profile_view.set_songs_view(songs_view)

    print(textwrap.dedent(
        r"""
         _  __ _ ___       __ __
        / \/  |_) | | ||\||_ (_
        \_/\__| \ | |_|| ||____)
        """
    ))

    while True:
        print()
        if not ctx.logged_in():
            account_view.display()
        else:
            profile_view.display()


def main():
    try:
        viewloop()
    except ExitStack:
        return


if __name__ == "__main__":
    main()
