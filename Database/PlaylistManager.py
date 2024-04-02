from DBConnector import DBConnector
import sys
import os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/src")
from saturn_cli import CommandLineParser


class PlaylistManager:
    """
    Focuses on handling playlist-related operations within the sound archive system, such as creating, modifying, and deleting playlists.

    Attributes:
        connector (PlaylistManager): An instance of the PlaylistManager class.
        sort_type (dict): A dictionary conPtaining different ways to sort a playlist. Keys represent sort options, and values provide descriptions or implementations of the sorting method.
        playlist_list(list): A list containing playlists. Each element in the list represents a playlist.

    Methods:
        view_sort_playlist: Sorts and displays the playlist by sound title, length, or date added to playlist.
        create_playlist: Creates a new playlist name. The new playlist name is added to playlist_list.
        play_sound_in_playlist: Plays a sound from one of the playlists. Plays using the play method in our CommandLineParser class
        add_sound_into_playlist: Adds a sound into a defined playlist.
        remove_sound_from_playlist: Removes a sound from a defined playlist.
    """

    def __init__(self, playlist_list):
        # composition relationship.
        self.connector = DBConnector("../sounds")
        self.sort_type = {"Title", "Length", "DateCreated"}
        self.playlist_list = playlist_list

    def view_sort_playlist(self, playlist_title, sort_name=None):
        # Verify playlist is valid.
        if playlist_title not in self.playlist_list:
            raise Exception(f"Invalid playlist: {playlist_title}")

        # OPEN CONNECTION.
        self.connector.open_connection()

        try:
            if sort_name:
                # Verify sort_name is valid.
                if sort_name not in self.sort_type:
                    raise Exception(f"Invalid sorting name: {sort_name}")

                # Sort playlist (database query here).
                self.connector.cursor.execute(
                    f"SELECT * FROM soundlist ORDER BY {sort_name}"
                )
            else:
                # Display all sounds in playlist_title.
                query = (
                    "SELECT SoundTitle FROM soundplaylistsinfo WHERE PlaylistTitle = %s"
                )
                self.connector.cursor.execute(query, (playlist_title,))

            results = self.connector.cursor.fetchall()
            for result in results:
                print(result)
            # self.connector.cnx.commit()  # Uncomment if needed.

        except Exception as e:
            print(f"Error showing playlist: {e}")

        finally:
            # CLOSE CONNECTION.
            self.connector.close_connection()

    def create_playlist(self, playlist_name):
        if playlist_name not in self.playlist_list:
            self.playlist_list.append(playlist_name)

    def play_sound_in_playlist(self, sound_title, sound_playlist):
        # verify sound_title and sound_playlist valid.
        if sound_title not in self.connector.sound_list:
            raise Exception(f"Invalid sound name: {sound_title}")

        if sound_playlist not in self.playlist_list:
            raise Exception(f"Invalid playlist name: {sound_playlist}")

        # play the sound.
        parser = CommandLineParser(sys.argv)
        parser.play(parent_dir + "/sounds/" + sound_title + ".wav")

    def add_sound_into_playlist(self, sound_title, sound_playlist):
        # verify sound_title, sound_playlist exits.
        print("njevnjcrevbrbfjvenjfvnej")
        print(self.connector.sound_list)
        if (
            sound_title not in self.connector.sound_list
            or sound_playlist not in self.playlist_list
        ):
            raise Exception(f"Invalid sound name: {sound_title}")

        if sound_playlist not in self.playlist_list:
            raise Exception(f"Invalid playlist name: {sound_playlist}")

        # TODO: verify sound_title not already in sound_playlist; database lookup.

        # insert it.
        self.connector.open_connection()
        query = (
            "INSERT INTO soundplaylistsinfo (SoundTitle, PlaylistTitle) VALUES (%s, %s)"
        )
        values = (sound_title, sound_playlist)
        try:
            self.connector.open_connection()
            self.connector.cursor.execute(query, values)
            self.connector.cnx.commit()
        except Exception as e:
            print(f"Error adding sound to playlist: {e}")
        finally:
            self.connector.close_connection()

    def remove_sound_from_playlist(self, sound_title, sound_playlist):
        # verify sound_title and sound_playlist valid.
        if (
            sound_title not in self.connector.sound_list
            or sound_playlist not in self.playlist_list
        ):
            raise Exception(
                f"Invalid sound name: {sound_title} or playlist name: {sound_playlist}"
            )


if __name__ == "__main__":
    manager = PlaylistManager(["Your Library"])
    manager.connector.init_playlist()

    print(f"Playlists: {manager.playlist_list}")
    print(f"Sound library: {manager.connector.sound_list}")

    # Example: create Liked playlist + add sounds into Liked.
    manager.create_playlist("Liked")

    manager.add_sound_into_playlist("coffee-slurp-2", "Liked")
    manager.add_sound_into_playlist("toaster-2", "Liked")
    manager.add_sound_into_playlist("coffee", "Liked")

    # view liked sorted vs unsorted.
    print("Songs in Liked Playlist (unsorted)")
    manager.view_sort_playlist("Liked")

    print("Songs in Liked Playlist (sorted by title)")
    manager.view_sort_playlist("Your Library", "Title")

    # playing a sound.
    manager.play_sound_in_playlist("toaster", "Your Library")
    """"""
