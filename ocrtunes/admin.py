import sys
from ocrtunes import database
from ocrtunes.database import songs
from ocrtunes.views import format_time


def main():
    db = database.initialise_db()
    if len(sys.argv) == 1:
        print("Usage: python -m ocrtunes.admin <genres|songs>")
    elif sys.argv[1] == "genres":
        genres = songs.get_genres(db)
        for genre in genres:
            length = songs.get_average_length(db, genre)
            print("Genre:", genre)
            print("Average length:", format_time(length))
            print()


if __name__ == "__main__":
    main()
