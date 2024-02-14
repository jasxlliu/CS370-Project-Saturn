import sys
import os
import threading
import simpleaudio as sa
import vlc

class CommandLineParser:
    """
    A class that parses command line arguments and executes corresponding commands.

    Args:
        argv (list): The list of command line arguments.

    Attributes:
        argv (list): The list of command line arguments.
        argvlen (int): The length of the command line arguments.
        isPlaying (bool): A flag indicating whether audio is currently being played.

    Methods:
        print_help(): Prints the help message with available commands.
        count_arguments(): Counts the number of arguments passed.
        play(file_path): Plays an audio file.
        play_overlap(queue): Plays multiple audio files overlapping each other.
        play_sequential(queue): Plays multiple audio files sequentially.
        play_command(): Executes the play command.
        overlap_command(): Executes the overlap command.
        sequential_command(): Executes the sequential command.
        list_command(): Lists all audio files in the current directory recursively.
        rename_command(): Renames an audio file.
        parse_arguments(): Parses the command line arguments and executes the corresponding command.
    """
    def __init__(self, argv):
        # initialize the command line parser
        self.argv = argv
        self.argvlen = len(argv)
        self.isPlaying = False
        self.audioFormats = [".wav", ".mp3", ".ogg", ".flac", ".m4a", ".wma", ".aiff", ".alac", ".aac", ".amr", ".au", ".awb", ".dct", ".dss", ".dvf", ".gsm", ".iklax", ".ivs", ".m4p", ".mmf", ".mpc", ".msv", ".nmf", ".nsf", ".oga", ".mogg", ".opus", ".ra", ".rm", ".raw", ".sln", ".tta", ".vox", ".wv", ".webm", ".8svx"]

    def print_help(self):
        print("usage:", "python", self.argv[0], "--help")
        # print all commands and what they do
        print("Commands:")
        print("-h,--help\t\tprint this help message.")
        print("-c,--count\t\tcount the number of arguments.")
        print("-p,--play\t\tplay a file.")
        print("-s,--sequential\t\tplay files sequentially.")
        print("-o,--overlap\t\tplay files overlapping each other.")
        print("-l,--list\t\tlist all audio files in the current directory recursively.")
        print("-r,--rename\t\trename an audio file.")
        sys.exit(0)

    def count_arguments(self):
        # count the number of arguments passed
        print(
            "counted ",
            self.argvlen - 2,
            " argument" + "s" if self.argvlen - 2 > 1 else "",
        )
        sys.exit(0)

    def play(self, file_path):
        # play a file using the simpleaudio library
        if file_path[-4:] == ".wav":
            self.isPlaying = True
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
            self.isPlaying = False
        else:
            self.isPlaying = True
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(file_path)
            media.get_mrl()
            player.set_media(media)
            player.play()
            while player.is_playing():
                continue
            self.isPlaying = False

    def play_overlap(self, queue):
        # play files overlapping using the play method
        # and threading to play multiple files at the same time
        threads = []
        for file_path in queue:
            thread = threading.Thread(target=self.play, args=(file_path,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def play_sequential(self, queue):
        # play files sequentially using the play method
        while not self.isPlaying and queue:
            for file_path in queue:
                print("Playing:", file_path)
                self.play(file_path)
                queue = queue[1:]


    def play_command(self):
        # play a file using the play method
        if self.argvlen > 2:
            file_path = self.argv[2]
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print("I am now playing", file_path)
            self.play(file_path)
        else:
            print(
                "Error: Please provide a file path after the --play or -p option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def overlap_command(self):
        # play files overlapping using the play_overlap method
        file_paths = []
        if self.argvlen > 2:
            for i in self.argv[2:]:
                file_paths.append(i)
                print("I am now playing files overlapping each other:", i)
            self.play_overlap(file_paths)
        else:
            print(
                "Error: Please provide file paths after the --overlap or -o option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def sequential_command(self):
        # play files sequentiall using the play method
        file_paths = []
        if self.argvlen > 2:
            for i in self.argv[2:]:
                file_paths.append(i)
            print(file_paths)
            self.play_sequential(file_paths)
        else:
            print(
                "Error: Please provide file paths after the --sequential or -s option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def list_command(self):
        #print all files in the current directory recursively with audio file extensions
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file[-4:] in self.audioFormats or file[-5:] in self.audioFormats or file[-6:] in self.audioFormats or file[-3:] in self.audioFormats:
                    print(os.path.join(root, file))

    def rename_command(self):
        # rename an audio file, take the original name and the new one, doesn't change file extension
        if self.argvlen > 3:
            original_name = self.argv[2]
            new_name = self.argv[3]
            os.rename(original_name, new_name)
        else:
            print(
                "Error: Please provide two arguments after after the --rename or -r option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def parse_arguments(self):
        # parse the command line arguments and execute the corresponding command
        command = self.argv[1] if len(self.argv) > 1 else None

        match command:
            case None | "--help" | "-h":
                self.print_help()
            case "-c" | "--count":
                self.count_arguments()
            case "-p" | "--play":
                self.play_command()
            case "-s" | "--sequential":
                self.sequential_command()
            case "-o" | "--overlap":
                self.overlap_command()
            case "-l" | "--list":
                self.list_command()
            case "-r" | "--rename":
                self.rename_command()
            case _:
                errors = self.argv[1:]
                print(
                    self.argv[0],
                    "error, unexpected arguments ",
                    errors,
                    file=sys.stderr,
                )
                print("Try", self.argv[0], "--help")
                sys.exit(1)

if __name__ == "__main__":
    # create a command line parser and parse the command line arguments
    parser = CommandLineParser(sys.argv)
    parser.parse_arguments()
