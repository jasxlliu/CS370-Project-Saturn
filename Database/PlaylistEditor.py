import wave
import os
from datetime import datetime
import mysql.connector

class PlaylistEditor:
    """
    Represents a playlist management system for storing sounds in a MySQL database.

    Attributes:
        None (No specific attributes defined in this class)

    Methods:
        __init__(self):
            Initializes the Playlist object. Creates a connection to the MySQL database.

        create_database_connection(self):
            Establishes a secure connection to the MySQL Workbench.
        
        init_playlist(self):
            Initializes soundlist table in database based on the sounds in the sounds directory.

        create(self):
            Adds an option for the user to create a new playlist.
            TODO: Show updates related to playlist creation in the MySQL Workbench.

        add_sound(self):
            Allows the user to add a sound to an existing playlist.
            TODO: Implement the logic for adding sounds to the playlist.

        remove_sound(self, sound_title):
            Enables the user to remove a sound from an existing playlist.
            TODO: Implement the logic for removing sounds from the playlist.
    """
    def __init__(self, sound_dir):
        self.sound_dir = sound_dir
        self.cnx = None
        self.cursor = None
        # self.connect_to_my_sql()
    
    def open_connection(self):
        print("<<Opening>> connection to MySQL")
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
            self.cursor = self.cnx.cursor()
            print("Connected to MySQL")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Could not connect to MySQL:", err)
                
    def close_connection(self):
        print("<<Closing>> connection to MySQL")
        self.cnx.close()
        print(self.cursor)
        self.cursor.close()
    
    def init_playlist(self):
        self.open_connection()
        
        # Create a cursor object to execute SQL queries
        # cursor = self.cnx.cursor()

        # SQL query to insert data from our sounds directory into a table
        insert_query = ("INSERT INTO soundlist"
                        "(Title, Length, IsEdited, DateCreated) "
                        "VALUES (%s, %s, %s, %s)")

        for filename in os.listdir(self.sound_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(self.sound_dir, filename)
                # Get the title from the filename (remove the extension)
                title = os.path.splitext(filename)[0]

                # SQL query to check if the title already exists in the table
                check_query = "SELECT COUNT(*) FROM soundlist WHERE Title = %s"
                self.cursor.execute(check_query, (title,))
                result = self.cursor.fetchone()

                if result[0] > 0:
                    print(f"{title} already exists in the database.")
                    continue

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

                data = (title, duration, is_edited, date_created)

                # Execute the query
                self.cursor.execute(insert_query, data)

        # Commit changes to the database
        self.cnx.commit()
        print("Data in sounds directory inserted successfully")

        # Close cursor and connection
        # cursor.close()
        self.close_connection()
    
    def create(self):
        pass
    
    def add_sound(self):
        pass
    
    def remove_sound(self, sound_title):
        pass