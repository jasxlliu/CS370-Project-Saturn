# NOTE: Install dependencies with `python -m pip install -r ./requirements.txt` in the root directory of the project

# NOTE: This requires ffmpeg to be installed on your system
- if on windows, use `scoop install ffmpeg`
- if on mac, use `brew install ffmpeg`
- if on linux use your package manager to install ffmpeg
  - ex. `sudo apt-get install ffmpeg`
  - ex. `sudo pacman -S ffmpeg`
  - ex. `sudo dnf install ffmpeg`

## CONNECTING TO MYSQL WORKBENCH
- [x] Start by downloading the SQLTools extension developed by Matheus Teixeira.
- [x] Navigate to SQLtools extensions, accessible from the left panel.
- [x] Click on "add new connection", then select "Search VSCode marketplace".
- [x] Locate and install "SQLTools MySQL/MariaDB" from the available options, typically found as the first link.
- [x] On SQLTools Settings tab, click on MySQL and enter the following information...
- [x] Connection name: saturn_sql
- [x] Server Address: localhost
- [x] Port: 3307
- [x] Username: root
- [x] Password word: whatever you want but I suggest Ask on connect. Here is the password: !WhitmanMemo08?
- [x] Test/save the connection.
- [x] Before running SQL commands each time, make sure you connect/disconnect to the database. You can use the SQLTools to view tables/data of our playlists.

# Project Saturn                                                                                 
**TODO:**       
- [ ] tests!!!!
- [ ] comments (new and update big block comment under class name)
- [ ] update documetation.md with new functions


**DONE:**
- [x] play function
- [x] -p flag : calls play function
- [x] sequential play function
- [x] overlapping play function
- [x] -s : calls sequential play function
- [x] -o : calls overlapping play function
- [x] suppress error messages
- [x] mp3 flac etc support!!!!

## EPOCH ONE REQS
- [x] A user must be able to interact with your program from the command line via a simple text-based interface.
- [x] From that command-line interface, the user should be able to get a list of available commands.
- [x] A user must be able to get a list of available sounds to play.
- [x] A user must be able to play back a single sound.
- [x] A user must be able to listen to multiple sounds simultaneously (i.e., layer multiple sounds on top of each other).
- [x] A user must be able to listen to a sequence of sounds.
- [x] A user must be able to rename a sound.
- [x] These requirements may be met either with a single large command-line program that implements all of them, or by a suite of smaller command-line programs that focus on a subset of features

## Group members
- Neel Troeger
- Chris Gomez
- Aidan von Buschwaldt
- Jas Liu
