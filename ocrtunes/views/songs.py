from ocrtunes.views import getchoice, ExitStack, format_time
from ocrtunes.database import songs, playlist
import math


class SongsView:
    page_length = 5

    def __init__(self, ctx):
        # Store context as attr
        self.ctx = ctx
        # Pagination variables
        self.page = 0
        self.songs = []
        self.total_pages = 0
        self.query = ""

    def display(self):
        # Show menu choice
        print()
        print("1) View all songs")
        print("2) Search songs")
        print("3) Export artist discography")
        print("4) Exit")
        choice = getchoice("Enter choice: ", ["1", "2", "3"])
        if choice == "1":
            self.view_all_songs()
        elif choice == "2":
            self.search_songs()
        elif choice == "3":
            self.export_songs()
        elif choice == "4":
            return

    def view_all_songs(self):
        self.query = ""
        self.setup_pages(songs.get_all_songs(self.ctx.db))
        self.view_songs()

    def search_songs(self):
        total = songs.get_library_size(self.ctx.db)
        print()
        print(f"Searching {total} songs")
        self.query = input("Enter query: ").strip()
        self.setup_pages(songs.search_songs(self.ctx.db, self.query))
        self.view_songs()

    def export_songs(self):
        print()
        artist = input("Enter artist (leave empty to quit): ").strip()
        if not artist:
            return
        song_list = songs.get_artist_songs(self.ctx.db, artist)
        if not song_list:
            print(f"Artist '{artist}' not found")
        with open(artist + ".txt", "w+") as f:
            for song in song_list:
                f.write(song + "\n")
        print(f"Exported list of songs by '{artist}'")

    def view_songs(self):
        self.page = 0

        while True:
            print()
            if not self.query:
                print(f"Showing all songs ({len(self.songs)})")
            else:
                print(f"Showing all songs matching '{self.query}' ({len(self.songs)})")
            if len(self.songs) == 0:
                print("No matching songs found")
                break

            options = ["p", "n", "q"]
            start = self.page * self.page_length
            i = start
            for song in self.songs[start: start + self.page_length]:
                i += 1
                print(f"{i}. " + song[1])
                options.append(str(i))
            print(f"Page {self.page + 1} of {self.total_pages}")

            choice = getchoice("Enter choice (song number / [p]revious / [n]ext / [q]uit): ", options)
            if choice.isdecimal():
                song_id = self.songs[int(choice) - 1][0]
                self.display_song_info(song_id)
            elif choice == "p":
                self.page = (self.page - 1) % self.total_pages
            elif choice == "n":
                self.page = (self.page + 1) % self.total_pages
            elif choice == "q":
                break

    def process_list(self, songs):
        out = []
        for row in songs:
            out.append((row[0], f"{row[1]} - {row[2]} {format_time(row[3])}"))
        return out

    def setup_pages(self, songs):
        self.page = 0
        self.songs = self.process_list(songs)
        self.total_pages = math.ceil(len(songs) / self.page_length)

    def display_song_info(self, song):
        title, artist, genre, length = songs.get_song_info(self.ctx.db, song)
        print()
        print("Title:", title)
        print("Artist:", artist, f"({songs.get_artist_count(self.ctx.db, artist)})")
        print("Genre:", genre, f"({songs.get_genre_count(self.ctx.db, genre)})")
        print("Length:", format_time(length))

        print("1) Add to playlist")
        print("2) Exit")
        choice = getchoice("Enter choice: ", ["1", "2"])
        if choice == "1":
            self.playlist_add_song(song)
        elif choice == "2":
            return

    def playlist_add_song(self, song):
        print()
        options = ["q"]
        playlists = playlist.get_all_playlists(self.ctx.db, self.ctx.user)
        if playlists:
            for i, id in enumerate(playlists):
                name = playlist.get_playlist_name(self.ctx.db, id)
                print(f"{i + 1}. {name}")
                options.append(str(i + 1))
        else:
            print("No playlists found")
            return

        choice = getchoice("Select playlist (or [q]uit): ", options)
        if choice == "q":
            return

        name = playlist.get_playlist_name(self.ctx.db, playlists[int(choice) - 1])
        if playlist.check_song_in_playlist(self.ctx.db, playlists[int(choice) - 1], song):
            print(f"Song is already in playlist {name}")
        else:
            playlist.add_song_to_playlist(self.ctx.db, playlists[int(choice) - 1], song)
            print(f"Successfully added to '{name}'")
