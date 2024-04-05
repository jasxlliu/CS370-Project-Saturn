import sys
import os
import threading
import simpleaudio as sa
from pydub import AudioSegment
import pydub.playback as playback
import pydub.effects as effects


class Saturn:
    """
    The Saturn class represents a command-line interface for audio file manipulation.

    Attributes:
        argv (list): The list of command-line arguments.
        argvlen (int): The length of the argv list.
        isPlaying (bool): Indicates whether an audio file is currently being played.
        audioFormats (list): A list of supported audio file formats.

    Methods:
        getInstance(): Returns an instance of the Saturn class.
        print_help(): Prints the help message with available commands and their usage.
        count_arguments(): Counts the number of arguments passed.
        play(file_path): Plays an audio file.
        play_overlap(queue): Plays multiple audio files overlapping each other.
        play_sequential(queue): Plays multiple audio files sequentially.
        play_command(): Executes the play command.
        overlap_command(): Executes the overlap command.
        sequential_command(): Executes the sequential command.
        list_command(): Lists all audio files in the current directory.
        rename_command(): Renames an audio file.
        transcode_command(): Changes the audio format of a file.
        play_backwards_command(): Plays an audio file backwards.
    """

    def __init__(self, argv, argvlen):

        self.argv = argv
        self.argvlen = argvlen

        self.isPlaying = False
        # small list of audio formats
        # necessary for the list command
        self.audioFormats = [
            ".wav",
            ".mp3",
            ".ogg",
            ".flac",
            ".m4a",
            ".wma",
            ".aiff",
            ".alac",
            ".aac",
            ".amr",
            ".au",
            ".awb",
            ".dct",
            ".dss",
            ".dvf",
            ".gsm",
            ".iklax",
            ".ivs",
            ".m4p",
            ".mmf",
            ".mpc",
            ".msv",
            ".nmf",
            ".nsf",
            ".oga",
            ".mogg",
            ".opus",
            ".ra",
            ".rm",
            ".raw",
            ".sln",
            ".tta",
            ".vox",
            ".wv",
            ".webm",
            ".8svx",
        ]

    def getInstance(self):
        return self

    def print_help(self):
        # this is hacky, but it is the only way to get the help message to print nicely without too much work
        # do not change it unless you can get the same output with less code
        print(
            "Commands:            Description:                                 Usage:"
        )
        print(
            "-h,--help            Print this help message.                     python {} --help".format(
                self.argv[0]
            )
        )
        print(
            "-c,--count           Count the number of arguments.               python {} --count".format(
                self.argv[0]
            )
        )
        print(
            "-p,--play            Play a file.                                 python {} --play file_path".format(
                self.argv[0]
            )
        )
        print(
            "-s,--sequential      Play files sequentially.                     python {} --sequential file_path1 file_path2 ...".format(
                self.argv[0]
            )
        )
        print(
            "-o,--overlap         Play files overlapping each other.           python {} --overlap file_path1 file_path2 ...".format(
                self.argv[0]
            )
        )
        print(
            "-l,--list            List audio files in the current directory.   python {} --list".format(
                self.argv[0]
            )
        )
        print(
            "-r,--rename          Rename an audio file.                        python {} --rename original_name new_name".format(
                self.argv[0]
            )
        )
        print(
            "-t,--transcode       Change audio format.                         python {} --transcode original_file.wav new_file.mp3".format(
                self.argv[0]
            )
        )
        print(
            "-b,--play-backwards  Play a file backward.                        python {} --play-backwards file_path".format(
                self.argv[0]
            )
        )
        print(
            "-a,--concatenate     Concatenate audio files.                     python {} --concatenate file1 file2 file3 ... name.extension crossfade".format(
                self.argv[0]
            )
        )
        sys.exit(0)

    def count_arguments(self):
        # count the number of arguments passed
        print(
            "counted ",
            self.argvlen - 2,
            " argument" + "s" if self.argvlen - 2 > 1 else "",
        )
        sys.exit(0)

    def getSound(self, file_path):
        return AudioSegment.from_file(
            file_path,
            format=(
                file_path.split(".")[-1]
                if file_path[0] != "."
                else file_path[1:].split(".")[-1]
            ),
        )

    def play(self, file_path):
        # play an audio file
        self.isPlaying = True
        sound = self.getSound(file_path)
        playback.play(sound)
        self.isPlaying = False

    def play_overlap(self, queue):
        # play files overlapping using the play method
        # and threading to play multiple files at the same time
        threads = []
        print(f"I am now playing the following overlapping each other: {queue}")
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
            self.play_overlap(file_paths)
        else:
            print(
                "Error: Please provide file paths after the --overlap or -o option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def sequential_command(self):
        # play files sequentially using the play method
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
        # print all files in the current directory recursively with audio file extensions
        # this WILL not work if the cwd is /src/
        # dirs is necessary for the os.walk function, don't remove it
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(tuple(self.audioFormats)):
                    print(os.path.join(root, file))

    def rename_command(self):
        # rename an audio file, take the original name and the new one, doesn't change file extension
        if self.argvlen > 3:
            original_name = self.argv[2]
            extension = (
                original_name.split(".")[-1]
                if original_name[0] != "."
                else original_name[1:].split(".")[-1]
            )
            new_name = self.argv[3]
            if "." not in new_name[1:] or "." not in original_name[1:]:
                print("Error: Please provide the file extension(s).", file=sys.stderr)
                sys.exit(1)
            elif original_name[1:].split(".")[-1] != new_name[1:].split(".")[-1]:
                print(
                    "This function does not convert between audio formats. Using original file extension..."
                )
            new_name = (
                new_name.split(".")[0]
                if new_name[0] != "."
                else "." + new_name[1:].split(".")[0] + "." + extension
            )
            os.rename(original_name, new_name)
        else:
            print(
                "Error: Please provide two arguments after after the --rename or -r option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def transcode_command(self):
        # Change audio format
        # Usage: python saturn_cli.py -t original_file new_file
        if self.argvlen == 4:
            original_file = self.argv[2]
            new_file = self.argv[3]

            # Determine file extensions
            original_extension = (
                original_file.split(".")[-1]
                if original_file[0] != "."
                else original_file[1:].split(".")[-1]
            )
            new_extension = (
                new_file.split(".")[-1]
                if new_file[0] != "."
                else new_file[1:].split(".")[-1]
            )

            # Load the audio and export it to the new format
            sound = AudioSegment.from_file(original_file, format=original_extension)
            sound.export(new_file, format=new_extension)
            print(
                f"File transcoded successfully from {original_extension} to {new_extension}"
            )

        else:
            print("Error: Please provide two arguments after the -t option.")
            sys.exit(1)

    def play_backwards_command(self):
        # play a file using the play method
        if self.argvlen > 2:
            file_path = self.argv[2]
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print("I am now playing", file_path)
            self.isPlaying = True
            # can't use the play function because it only takes the file path.
            # this will have to be ammended in the future
            # TODO ^
            sound = AudioSegment.from_file(
                file_path,
                format=(
                    file_path.split(".")[-1]
                    if file_path[0] != "."
                    else file_path[1:].split(".")[-1]
                ),
            )
            playback.play(sound.reverse())
            self.isPlaying = False
        else:
            print(
                "Error: Please provide a file path after the --play or -p option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def concatenate_command(self):
        # concatenate audio files with crossfade amount (if not supplied, then 0)
        # python saturn_cli.py -a file1 file2 file3 ... new_name.extension crossfade
        if self.argvlen > 4:
            file_paths = self.argv[2:-3]
            new_name = self.argv[-2]
            extension = new_name.split(".")[-1]
            crossfade = self.argv[-1] if self.argv[-1].isdigit() else 0
            if "." not in new_name[1:]:
                print("Error: Please provide the file extension.", file=sys.stderr)
                sys.exit(1)
            new_name = (
                new_name.split(".")[0]
                if new_name[0] != "."
                else "." + new_name[1:].split(".")[0] + "." + extension
            )
            sounds = [AudioSegment.from_file(f) for f in file_paths]
            combined = sounds[0]
            for sound in sounds[1:]:
                combined = combined.append(sound, crossfade=0)
            combined.export(new_name, format=extension)
        else:
            print(
                "Error: Please provide at least two file paths and a new name with extension after the --concatenate or -a option.",
                file=sys.stderr,
            )
            sys.exit(1)


class CommandLineParser:
    """
    A class that parses command line arguments and executes corresponding commands.

    Attributes:
        argv (list): The list of command line arguments.

    Methods:
        __init__(self, argv): Initializes the CommandLineParser object.
        parse_arguments(self): Parses the command line arguments and executes the corresponding command.
    """

    def __init__(self, argv):
        self.argv = argv
        self.saturn = Saturn(self.argv, len(self.argv))
        self.parse_arguments()

    def parse_arguments(self):
        """
        Parses the command line arguments and executes the corresponding command.
        """
        command = self.argv[1] if len(self.argv) > 1 else None

        match command:
            case None | "--help" | "-h":
                self.saturn.print_help()
            case "-c" | "--count":
                self.saturn.count_arguments()
            case "-p" | "--play":
                self.saturn.play_command()
            case "-s" | "--sequential":
                self.saturn.sequential_command()
            case "-o" | "--overlap":
                self.saturn.overlap_command()
            case "-l" | "--list":
                self.saturn.list_command()
            case "-r" | "--rename":
                self.saturn.rename_command()
            case "-t" | "--transcode":
                self.saturn.transcode_command()
            case "-b" | "--play-backwards":
                self.saturn.play_backwards_command()
            case "-a" | "--concatenate":
                self.saturn.concatenate_command()
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
