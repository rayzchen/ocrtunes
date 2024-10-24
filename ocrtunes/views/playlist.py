from ocrtunes.views import getchoice, ExitStack, format_time
from ocrtunes.database import playlist, songs
import math


class PlaylistView:
    page_length = 5

    def __init__(self, ctx):
        # Store context as attr
        self.ctx = ctx
        # Pagination variables
        self.page = 0
        self.songs = []
        self.total_pages = 0

    def display(self):
        while True:
            print()
            options = ["n", "q"]
            playlists = playlist.get_all_playlists(self.ctx.db, self.ctx.user)
            if playlists:
                for i, id in enumerate(playlists):
                    name = playlist.get_playlist_name(self.ctx.db, id)
                    print(f"{i + 1}. {name}")
                    options.append(str(i + 1))
            else:
                print("No playlists found")

            choice = getchoice("Select playlist (or [n]ew / [q]uit): ", options)
            if choice == "n":
                self.create_playlist()
            elif choice == "q":
                break
            else:
                self.view_playlist(playlists[int(choice) - 1])

    def create_playlist(self):
        print()
        print("1) Create blank playlist")
        print("2) Create playlist from genre")
        print("3) Create playlist from duration")
        print("4) Quit")

        choice = getchoice("Enter choice: ", ["1", "2", "3", "4"])
        if choice == "4":
            return

        print("Creating new playlist")
        name = input("Enter new playlist name (leave empty to quit): ").strip()
        if not name:
            return

        if choice == "1":
            playlist.create_playlist(self.ctx.db, self.ctx.user, name)
            print(f"Successfully created playlist '{name}'")
        elif choice == "2":
            genre = input("Enter genre (leave empty to quit): ").strip()
            if genre not in songs.get_genres(self.ctx.db):
                print(f"No songs matching genre '{genre}'")
            playlist.create_genre_playlist(self.ctx.db, self.ctx.user, name, genre)
        elif choice == "3":
            duration = ""
            while True:
                duration = input(
                    "Enter duration in mins (leave empty to quit): "
                ).strip()
                if not duration.isdecimal():
                    print("Invalid duration!")
                else:
                    break
            playlist.create_duration_playlist(
                self.ctx.db, self.ctx.user, name, int(duration)
            )

    def view_playlist(self, id):
        name = playlist.get_playlist_name(self.ctx.db, id)
        size = playlist.get_playlist_size(self.ctx.db, id)
        length = playlist.get_playlist_length(self.ctx.db, id)

        print()
        print("Title:", name)
        print("Number of songs:", size)
        print("Total length:", format_time(length))
        print("1) List songs")
        print("2) Rename playlist")
        print("3) Delete playlist")
        print("4) Exit")
        choice = getchoice("Enter choice: ", ["1", "2", "3", "4"])
        if choice == "1":
            self.list_songs(id)
        elif choice == "2":
            self.rename_playlist(id)
        elif choice == "3":
            self.delete_playlist(id)
        elif choice == "4":
            return

    def process_list(self, songs):
        out = []
        for row in songs:
            out.append((row[0], f"{row[1]} - {row[2]} {format_time(row[3])}"))
        return out

    def list_songs(self, id):
        self.songs = self.process_list(playlist.get_playlist_songs(self.ctx.db, id))
        self.page = 0
        self.total_pages = math.ceil(len(self.songs) / self.page_length)
        if not self.songs:
            print()
            print("No songs found")
            return
        while True:
            print()
            print(f"Total number of songs: {len(self.songs)}")
            start = self.page * self.page_length
            i = start
            for song in self.songs[start : start + self.page_length]:
                i += 1
                print(f"{i}. " + song[1])
            print(f"Page {self.page + 1} of {self.total_pages}")

            choice = getchoice(
                "Enter choice ([p]revious / [n]ext / [q]uit): ", ["p", "n", "q"]
            )
            if choice == "p":
                self.page = (self.page - 1) % self.total_pages
            elif choice == "n":
                self.page = (self.page + 1) % self.total_pages
            elif choice == "q":
                break

    def rename_playlist(self, id):
        print()
        name = playlist.get_playlist_name(self.ctx.db, id)
        print(f"Renaming playlist '{name}'")
        name = self.get_playlist_name()
        playlist.rename_playlist(self.ctx.db, id, name)
        print(f"Successfully renamed playlist to '{name}'")

    def delete_playlist(self, id):
        print()
        name = playlist.get_playlist_name(self.ctx.db, id)
        print(f"Deleting playlist '{name}'")
        choice = getchoice(
            "Are you sure you want to delete this playlist? (y/n) ", ["y", "n"]
        )
        if choice == "y":
            playlist.delete_playlist(self.ctx.db, id)
            print(f"Successfully deleted playlist")
