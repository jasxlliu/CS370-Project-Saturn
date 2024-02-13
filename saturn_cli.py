import sys
import os
import threading
import simpleaudio as sa


class CommandLineParser:
    def __init__(self, argv):
        self.argv = argv
        self.argvlen = len(argv)
        self.isPlaying = False

    def print_help(self):
        print("usage:", self.argv[0], "--help")
        # print all commands and what they do
        print("Commands:")
        print("  -h, --help", "                 ", "print this help message.")
        print("  -c, --count", "                ", "count the number of arguments.")
        print("  -p, --play", "                 ", "play a file.")
        print("  -s, --sequential", "           ", "play files sequentially.")
        print("  -o, --overlap", "              ", "play files overlapping each other.")
        print("  -l, --list", "                 ", "list all wav files in the current directory recursively")
        print("  -r, --rename", "               ", "rename an audio file.")
        sys.exit(0)

    def count_arguments(self):
        print(
            "counted ",
            self.argvlen - 2,
            " argument" + "s" if self.argvlen - 2 > 1 else "",
        )
        sys.exit(0)

    def play(self, file_path):
        self.isPlaying = True
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        self.isPlaying = False

    def play_overlap(self, queue):
        threads = []
        for file_path in queue:
            thread = threading.Thread(target=self.play, args=(file_path,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def play_sequential(self, queue):
        while not self.isPlaying and queue:
            for file_path in queue:
                print("Playing:", file_path)
                self.play(file_path)
                queue = queue[1:]

    def parse_arguments(self):
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

    def play_command(self):
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
        #print all files in the current directory recursively with *.wav extension
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(".wav"):
                    print(os.path.join(root, file))

    def rename_command(self):
        # rename an audio file, take the original name and the new one, doesn't change file extension
        if self.argvlen > 3:
            original_name = self.argv[2]
            new_name = self.argv[3]
            if original_name.endswith(".wav") and new_name.endswith(".wav"):
                os.rename(original_name, new_name)
            else:
                print(
                    "Error: Please provide a file path with .wav extension after the --rename or -r option.",
                    file=sys.stderr,
                )
                sys.exit(1)

if __name__ == "__main__":
    parser = CommandLineParser(sys.argv)
    parser.parse_arguments()
