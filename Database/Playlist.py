import wave
import os
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode

class Playlist:
    """
    Represents a playlist management system for storing sounds in a MySQL database.

    Attributes:
        None (No specific attributes defined in this class)

    Methods:
        __init__(self):
            Initializes the Playlist object. Creates a connection to the MySQL database.
            TODO: Initialize table SoundList to hold info on the default loaded sounds
                  from our GitHub sounds file (refer to UML diagram).

        create_database_connection(self):
            Establishes a secure connection to the MySQL Workbench.

        create(self):
            Adds an option for the user to create a new playlist.
            TODO: Show updates related to playlist creation in the MySQL Workbench.

        add_sound(self):
            Allows the user to add a sound to an existing playlist.
            TODO: Implement the logic for adding sounds to the playlist.

        remove_sound(self):
            Enables the user to remove a sound from an existing playlist.
            TODO: Implement the logic for removing sounds from the playlist.
    """
    def __init__(self, sound_dir):
        self.sound_dir = sound_dir
        self.connect_to_my_sql()
    
    def connect_to_my_sql(self):
        config = {
            'user': 'root',
            'password': '!WhitmanMemo08?',
            'host': '127.0.0.1',
            'port': 3307,
            'database': 'soundarchive',
            'raise_on_warnings': True
        }
        
        try:
            self.cnx = mysql.connector.connect(**config)
            print("Connected to MySQL")
            self.init_playlist()
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Could not connect to MySQL:", err)
    
    def init_playlist(self):
        # Create a cursor object to execute SQL queries
        cursor = self.cnx.cursor()
        
        # Example SQL query to insert data into a table
        insert_query = ("INSERT INTO soundlist"
                        "(Title, Length, IsEdited, DateCreated) "
                        "VALUES (%s, %s, %s, %s)")
        
        for filename in os.listdir(self.sound_dir):
            print(filename)
            if filename.endswith(".wav"):
                file_path = os.path.join(self.sound_dir, filename)
                # Get the title from the filename (remove the extension)
                title = os.path.splitext(filename)[0]

                try:
                    # Get the length of the .wav file
                    with wave.open(file_path, 'r') as wav_file:
                        frames = wav_file.getnframes()
                        rate = wav_file.getframerate()
                        duration = frames / float(rate)  # Duration in seconds
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue

                # Set IsEdited to False
                is_edited = False

                # Get the current date and time
                date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Data to be inserted into the table
                print("title: ", type(title))
                print("duration: ", type(duration))
                print("is_edited: ", type(is_edited))
                print("date_created: ", date_created)
                data = (title, duration, is_edited, date_created)
                
                # Execute the query
                cursor.execute(insert_query, data)

        # Commit changes to the database
        print("test")
        self.cnx.commit()
        print("Data inserted successfully")
        
        # Close cursor and connection
        cursor.close()
        self.cnx.close()
    
    def create(self):
        pass
    
    def add_sound(self):
        pass
    
    def remove_sound(self):
        pass

if __name__ == "__main__":
    # create a command line parser and parse the command line arguments
    playlist = Playlist("../sounds")