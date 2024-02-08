'''
CS-370 lab activity for Jan. 30, 2024
This file includes a sample example of how you can use sys.argv to parse command line arguments.
sys.argv is a list containing all the items that have been typed on the command line for a particular invocation of a program.

For example, you might type into the command line, to execute your python program:
>> python myprogram.py --dostuff arguments

sys.argv[0] is the name used to invoke the program (myprogram.py).
Optionally, additional arguments may come after the name of the program, those are sys.argv[1], etc.
'''

import sys
import os
import threading
import simpleaudio as sa
argvlen = len(sys.argv)

'''
This is a debugging statement that prints out the list of command line arguments that were included when you 
invoked this program from the command line.
'''
print("sys.argv: ", sys.argv)

'''
# HELP: This is a command line argument that is invoked by typing --help or -h
(Note that it is a command line convention to offer full name and first letter options.
The full name options have two preceding dashes -- and the one-letter options have just one -)
For example:
>> python cli_example.py --help
>> python cli_example.py --h

Right now, this help command is not very useful.
Take a look at some other helps commands, like
>> python --help
>> pip -h
>> conda --help
To see what they include.
'''

# This if statement checks to see what argument comes right after the program name
# Note that it also runs if you have no arguments after the program name
if argvlen<=1 or sys.argv[1]=='--help' or sys.argv[1]=='-h':

    # This prints out a sample of how you might use this command
    print("usage:",sys.argv[0], '--help')

    # Note that it is proper hygiene to have this at the end of each
    sys.exit(0);

'''
# HELP: This is another command line argument, invoked by typing --count or -c.
For example:
>> python cli_example.py --count
>> python cli_example.py -c *
'''
# Count is pretty basic: It just counts the command line arguments that come after it
if sys.argv[1] == '-c' or sys.argv[1] == '--count' :
    print("counted ", argvlen-2, " argument"+"s" if argvlen-2>1 else "")
    sys.exit(0)

'''
To add additional command line arguments, that have more capabilities, you need create more if statements.
For example, if we want to play a file, we should construct a new if statement to parse the following that you might 
enter into the command line:
>> python cli_example.py --play sounds/toaster.wav
>> python cli_example.py -p sounds/coffee.wav
'''

# TODO: Add in the play command by writing a new if statement
'''
You can use count as a template/example.
For now, it doesn't have to actually play a file, but it should take in a filepath as an additional argument
that comes after play (see the examples above).

For now, just have it print out the statement:
"I am now playing <filepath>."

(You'll add in the ability to actually play in the next step.)
'''


isPlaying = False

# this will be passed by the if statement below
def get_queue(queue_as_string):
    queue = queue_as_string.split()
    return queue

def play(file_path):
    isPlaying = True
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    isPlaying = False

def play_overlap(queue):
    threads = []
    for file_path in queue:
        thread = threading.Thread(target=play, args=(file_path, ))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def play_sequential(queue):
    # go through and play each sound in our list.
    while not isPlaying and queue != []:
        for file_path in queue:
            print("Playing:", file_path)
            play(file_path) # this should work, since play waits until the sound is done
            queue = queue[1:] # remove the first element from the list
                              # this prevents an infinite loop

# Check if the play command is given
if sys.argv[1] == '-p' or sys.argv[1] == '--play':
    # Ensure there is at least one more argument for the file path
    if argvlen > 2:
        file_path = sys.argv[2]
        if file_path[0] == ".":
            file_path = str(os.getcwd()) + file_path[1:]
        print("I am now playing", file_path)
        play(file_path)
    else:
        print("Error: Please provide a file path after the --play or -p option.", file=sys.stderr)
        sys.exit(1)

# Check if the play command with sequential flag is given
elif sys.argv[1] == '-s' or sys.argv[1] == '--sequential':
    file_paths = []
    # Ensure there is at least one more argument for the file path
    if argvlen > 2:
        for i in sys.argv[2:]:
            file_paths.append(i)
            #print("I am now playing files sequentially:", i)
        print(file_paths)
        play_sequential(file_paths)
    else:
        print("Error: Please provide file paths after the --sequential or -s option.", file=sys.stderr)
        sys.exit(1)

# Check if the play command with overlap flag is given
elif sys.argv[1] == '-t' or sys.argv[1] == '--top':
    file_paths = []
    # Ensure there is at least one more argument for the file path
    if argvlen > 2:
        # loop through the sound files (maybe not most efficient but can be changed later!)
        for i in sys.argv[2:]:
            file_paths.append(i)
            print("I am now playing files on top of each other:", i)
        play_overlap(file_paths)
    else:
        print("Error: Please provide file paths after the --top or -t option.", file=sys.stderr)
        sys.exit(1)


# ADD YOUR CODE FOR PLAY HERE


'''
This goes at the end of all of your if statements and it lets you know if you have 
unknown or unaddressed command line arguments.
'''
print(sys.argv[0], "error, unexpected arguments ", sys.argv[1:],file=sys.stderr)

sys.exit(1)
