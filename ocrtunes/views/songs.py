from ocrtunes.views import getchoice, ExitStack, format_time
from ocrtunes.database import songs
import math


class SongsView:
    page_length = 5

    def __init__(self, ctx):
        # Store context as attr
        self.ctx = ctx
        # Pagination variables
        self.page = 0
        self.songs = []
        self.query = ""

    def display(self):
        # Show menu choice
        print()
        print("1) View all songs")
        print("2) Search songs")
        print("3) Exit")
        choice = getchoice("Enter choice: ", ["1", "2", "3"])
        if choice == "1":
            self.view_all_songs()
        elif choice == "2":
            self.search_songs()
        elif choice == "3":
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
