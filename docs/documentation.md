# Command Line Audio Player

This is a simple command-line audio player written in Python. It allows you to play, list, and rename audio files, as well as play multiple files sequentially or overlapping.

## Usage

```bash
python src/saturn_cli.py [options] [arguments]
```

### Options

- `-h`, `--help`: Print the help message.
- `-c`, `--count`: Count the number of arguments.
- `-p`, `--play`: Play a single audio file.
- `-s`, `--sequential`: Play multiple audio files sequentially.
- `-o`, `--overlap`: Play multiple audio files overlapping each other.
- `-l`, `--list`: List all audio files in the current directory recursively.
- `-r`, `--rename`: Rename an audio file.

## Commands

### `play` Command

```bash
python src/saturn_cli.py --play file_path
```

- Play a single audio file specified by `file_path`.
- Note that file types other that `.wav` are not supported on Windows.

### `sequential` Command

```bash
python src/saturn_cli.py --sequential file1 file2 ... fileN
```

- Play multiple audio files sequentially. Provide the file paths as arguments.

### `overlap` Command

```bash
python src/saturn_cli.py --overlap file1 file2 ... fileN
```

- Play multiple audio files overlapping each other. Provide the file paths as arguments.

### `list` Command

```bash
python src/saturn_cli.py --list
```

- List all audio files in the current directory recursively.

### `rename` Command

```bash
python src/saturn_cli.py --rename original_name new_name
```

- Rename an audio file. Provide the original and new names as arguments.

## Examples

1. Display the help message:

```bash
python src/saturn_cli.py --help
```

2. Count the number of arguments:

```bash
python src/saturn_cli.py --count arg1 arg2 arg3
```

3. Play a single audio file:

```bash
python src/saturn_cli.py --play audio_file.wav
```

4. Play multiple audio files sequentially:

```bash
python src/saturn_cli.py --sequential file1.wav file2.wav file3.wav
```

5. Play multiple audio files overlapping:

```bash
python src/saturn_cli.py --overlap file1.wav file2.wav file3.wav
```

6. List all audio files in the current directory:

```bash
python src/saturn_cli.py --list
```

7. Rename an audio file:

```bash
python src/saturn_cli.py --rename old_name.wav new_name.wav
```

## Note

- Make sure to provide valid file paths and follow the specified command syntax.