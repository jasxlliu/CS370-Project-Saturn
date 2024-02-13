import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os
import threading
import simpleaudio as sa

from saturn_cli import CommandLineParser

class TestCommandLineParser(unittest.TestCase):
    def setUp(self):
        self.parser = CommandLineParser([])

    def test_print_help(self):
        expected_output = "usage: script_name --help\nCommands:\n  -h, --help                   print this help message.\n  -c, --count                  count the number of arguments.\n  -p, --play                   play a file.\n  -s, --sequential             play files sequentially.\n  -o, --overlap                play files overlapping each other.\n  -l, --list                   list all wav files in the current directory recursively.\n  -r, --rename                 rename an audio file.\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.parser.print_help()
            self.assertEqual(fake_out.getvalue(), expected_output)

    def test_count_arguments(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.parser.count_arguments()
            self.assertEqual(fake_out.getvalue(), "counted 0 arguments\n")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.parser.argv = ["script_name", "arg1", "arg2"]
            self.parser.count_arguments()
            self.assertEqual(fake_out.getvalue(), "counted 2 arguments\n")

    def test_play(self):
        file_path = "test.wav"
        expected_output = "I am now playing test.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.sa.WaveObject") as mock_wave_obj:
                mock_wave_obj.from_wave_file.return_value = mock_wave_obj
                mock_wave_obj.play.return_value = mock_wave_obj
                self.parser.play(file_path)
                self.assertEqual(fake_out.getvalue(), expected_output)
                mock_wave_obj.from_wave_file.assert_called_once_with(file_path)
                mock_wave_obj.play.assert_called_once()

    def test_play_overlap(self):
        queue = ["file1.wav", "file2.wav", "file3.wav"]
        expected_output = "I am now playing files overlapping each other: file1.wav\nI am now playing files overlapping each other: file2.wav\nI am now playing files overlapping each other: file3.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.threading.Thread") as mock_thread:
                self.parser.play_overlap(queue)
                self.assertEqual(fake_out.getvalue(), expected_output)
                self.assertEqual(mock_thread.call_count, len(queue))
                for i, thread in enumerate(mock_thread.call_args_list):
                    self.assertEqual(thread[0][0], self.parser.play)
                    self.assertEqual(thread[0][1], (queue[i],))

    def test_play_sequential(self):
        queue = ["file1.wav", "file2.wav", "file3.wav"]
        expected_output = "Playing: file1.wav\nPlaying: file2.wav\nPlaying: file3.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.CommandLineParser.play") as mock_play:
                self.parser.isPlaying = False
                self.parser.play_sequential(queue)
                self.assertEqual(fake_out.getvalue(), expected_output)
                self.assertEqual(mock_play.call_count, len(queue))
                for i, play in enumerate(mock_play.call_args_list):
                    self.assertEqual(play[0][0], queue[i])
                self.assertFalse(self.parser.isPlaying)

    def test_play_command(self):
        file_path = "test.wav"
        self.parser.argv = ["script_name", "--play", file_path]
        expected_output = "I am now playing test.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("os.getcwd") as mock_getcwd:
                mock_getcwd.return_value = "/home/morgan/projects/CS/CS370/CS370-Project-Saturn/"
                with patch("saturn_cli.sa.WaveObject") as mock_wave_obj:
                    mock_wave_obj.from_wave_file.return_value = mock_wave_obj
                    mock_wave_obj.play.return_value = mock_wave_obj
                    self.parser.play_command()
                    self.assertEqual(fake_out.getvalue(), expected_output)
                    mock_wave_obj.from_wave_file.assert_called_once_with("/home/morgan/projects/CS/CS370/CS370-Project-Saturn/test.wav")
                    mock_wave_obj.play.assert_called_once()

    def test_overlap_command(self):
        file_paths = ["file1.wav", "file2.wav", "file3.wav"]
        self.parser.argv = ["script_name", "--overlap"] + file_paths
        expected_output = "I am now playing files overlapping each other: file1.wav\nI am now playing files overlapping each other: file2.wav\nI am now playing files overlapping each other: file3.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.CommandLineParser.play_overlap") as mock_play_overlap:
                self.parser.overlap_command()
                self.assertEqual(fake_out.getvalue(), expected_output)
                mock_play_overlap.assert_called_once_with(file_paths)

    def test_sequential_command(self):
        file_paths = ["file1.wav", "file2.wav", "file3.wav"]
        self.parser.argv = ["script_name", "--sequential"] + file_paths
        expected_output = "file_paths\nPlaying: file1.wav\nPlaying: file2.wav\nPlaying: file3.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.CommandLineParser.play_sequential") as mock_play_sequential:
                self.parser.sequential_command()
                self.assertEqual(fake_out.getvalue(), expected_output)
                mock_play_sequential.assert_called_once_with(file_paths)

    def test_list_command(self):
        expected_output = "/home/morgan/projects/CS/CS370/CS370-Project-Saturn/test.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [("/home/morgan/projects/CS/CS370/CS370-Project-Saturn/", [], ["test.wav"])]
                self.parser.list_command()
                self.assertEqual(fake_out.getvalue(), expected_output)

    def test_rename_command(self):
        original_name = "old.wav"
        new_name = "new.wav"
        self.parser.argv = ["script_name", "--rename", original_name, new_name]
        with patch("os.rename") as mock_rename:
            self.parser.rename_command()
            mock_rename.assert_called_once_with(original_name, new_name)

    def test_parse_arguments_help(self):
        self.parser.argv = ["script_name", "--help"]
        expected_output = "usage: script_name --help\nCommands:\n  -h, --help                   print this help message.\n  -c, --count                  count the number of arguments.\n  -p, --play                   play a file.\n  -s, --sequential             play files sequentially.\n  -o, --overlap                play files overlapping each other.\n  -l, --list                   list all wav files in the current directory recursively.\n  -r, --rename                 rename an audio file.\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.parser.parse_arguments()
            self.assertEqual(fake_out.getvalue(), expected_output)

    def test_parse_arguments_count(self):
        self.parser.argv = ["script_name", "--count", "arg1", "arg2"]
        expected_output = "counted 2 arguments\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.parser.parse_arguments()
            self.assertEqual(fake_out.getvalue(), expected_output)

    def test_parse_arguments_play(self):
        file_path = "test.wav"
        self.parser.argv = ["script_name", "--play", file_path]
        expected_output = "I am now playing test.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("os.getcwd") as mock_getcwd:
                mock_getcwd.return_value = "/home/morgan/projects/CS/CS370/CS370-Project-Saturn/"
                with patch("saturn_cli.sa.WaveObject") as mock_wave_obj:
                    mock_wave_obj.from_wave_file.return_value = mock_wave_obj
                    mock_wave_obj.play.return_value = mock_wave_obj
                    self.parser.parse_arguments()
                    self.assertEqual(fake_out.getvalue(), expected_output)
                    mock_wave_obj.from_wave_file.assert_called_once_with("/home/morgan/projects/CS/CS370/CS370-Project-Saturn/test.wav")
                    mock_wave_obj.play.assert_called_once()

    def test_parse_arguments_sequential(self):
        file_paths = ["file1.wav", "file2.wav", "file3.wav"]
        self.parser.argv = ["script_name", "--sequential"] + file_paths
        expected_output = "file_paths\nPlaying: file1.wav\nPlaying: file2.wav\nPlaying: file3.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.CommandLineParser.play_sequential") as mock_play_sequential:
                self.parser.parse_arguments()
                self.assertEqual(fake_out.getvalue(), expected_output)
                mock_play_sequential.assert_called_once_with(file_paths)

    def test_parse_arguments_overlap(self):
        file_paths = ["file1.wav", "file2.wav", "file3.wav"]
        self.parser.argv = ["script_name", "--overlap"] + file_paths
        expected_output = "I am now playing files overlapping each other: file1.wav\nI am now playing files overlapping each other: file2.wav\nI am now playing files overlapping each other: file3.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("saturn_cli.CommandLineParser.play_overlap") as mock_play_overlap:
                self.parser.parse_arguments()
                self.assertEqual(fake_out.getvalue(), expected_output)
                mock_play_overlap.assert_called_once_with(file_paths)

    def test_parse_arguments_list(self):
        expected_output = "/home/morgan/projects/CS/CS370/CS370-Project-Saturn/test.wav\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [("/home/morgan/projects/CS/CS370/CS370-Project-Saturn/", [], ["test.wav"])]
                self.parser.parse_arguments()
                self.assertEqual(fake_out.getvalue(), expected_output)

    def test_parse_arguments_rename(self):
        original_name = "old.wav"
        new_name = "new.wav"
        self.parser.argv = ["script_name", "--rename", original_name, new_name]
        with patch("os.rename") as mock_rename:
            self.parser.parse_arguments()
            mock_rename.assert_called_once_with(original_name, new_name)

    def test_parse_arguments_error(self):
        self.parser.argv = ["script_name", "--invalid"]
        expected_output = "script_name error, unexpected arguments  ['--invalid']\nTry script_name --help\n"
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.parser.parse_arguments()
            self.assertEqual(fake_out.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()