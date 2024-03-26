import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ManageTags:
    def __init__(self, tags=None):
        # Initialize tags with an empty list or provided tags
        self.tags = tags if tags else []

    def __enter__(self):
        try:
            # Set up Google Sheets API credentials
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('./saturn-manage-tags-75ea5f585f59.json', scope)
            gc = gspread.authorize(credentials)

            # Open the spreadsheet by URL (you can also use the key)
            sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1RdV1p_4uHyulaHqmEWiahajxj9ZPFTMJy8j1VrR7L34/edit#gid=0')

            # Access the first worksheet
            worksheet = sh.sheet1  
            
            # kinda wanna start fresh everytime?
            worksheet.clear()

            # Example: Update cell A1 with a new value
            worksheet.append_row(['Title', 'Length', 'Date Created', 'Folders'])

            # This is how I'm thinking a sound tag import thing might look like.
            worksheet.append_row(['Coffee Slurp', '1.05 seconds', '2/27/2024 5:16 PM', '[Favorite, Chill Sound]'])

            # Return the worksheet object for further interactions
            return worksheet

        except Exception as e:
            print(f"Error setting up Google Sheets: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create_tag(self, tag_name):
        # Implement logic to add a new tag to self.tags
        self.tags.append(tag_name)
        print(f"Tag '{tag_name}' added successfully!")

    def favorite_tag(self, tag_name):
        # Implement logic to mark a tag as a favorite
        pass

    def remove_tag(self, tag_name):
        # Implement logic to remove a tag by name
        pass


if __name__ == "__main__":
    # Instantiate an object of the ManageTags class
    my_tags_manager = ManageTags(tags=['tag1', 'tag2', 'tag3'])

    # Example: Create a new tag
    my_tags_manager.create_tag("new_tag")

    # Example: Access the Google Sheets worksheet
    with my_tags_manager as worksheet:
        if worksheet:
            # Interact with the worksheet as needed
            pass
