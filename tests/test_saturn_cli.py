import unittest
from unittest.mock import patch
import sys

# import saturn_cli's CommandLineParser (located in ../src/saturn_cli.py)
sys.path.append("src")

from saturn_cli import CommandLineParser


class TestCommandLineParser(unittest.TestCase):
    def setUp(self):
        self.parser = CommandLineParser([])

    def test_play(self):
        # Provide a valid file path for testing
        file_path = "path/to/test.wav"
        with patch("saturn_cli.playback.play") as mock_play:
            self.parser.play(file_path)
            mock_play.assert_called_once_with(file_path)

    def test_play_overlap(self):
        # Test playing files overlapping
        with patch("saturn_cli.CommandLineParser.play") as mock_play:
            self.parser.play_overlap(["file1.wav", "file2.wav", "file3.wav"])
            self.assertEqual(mock_play.call_count, 3)

    def test_play_sequential(self):
        # Test playing files sequentially
        with patch("saturn_cli.CommandLineParser.play") as mock_play:
            self.parser.isPlaying = False
            self.parser.play_sequential(["file1.wav", "file2.wav", "file3.wav"])
            self.assertEqual(mock_play.call_count, 3)

    def test_play_command(self):
        with patch("sys.exit") as mock_exit:
            self.parser.play_command()
            mock_exit.assert_called_once_with(1)

        # Test play command with missing file path
        with patch("sys.stderr") as mock_stderr:
            self.parser.argv = ["", "", "--play"]
            self.parser.play_command()
            mock_stderr.write.assert_called_once()

    def test_overlap_command(self):
        with patch("sys.exit") as mock_exit:
            self.parser.overlap_command()
            mock_exit.assert_called_once_with(1)

    def test_sequential_command(self):
        with patch("sys.exit") as mock_exit:
            self.parser.sequential_command()
            mock_exit.assert_called_once_with(1)

        # Test sequential command with missing file paths
        with patch("sys.stderr") as mock_stderr:
            self.parser.argv = ["", "", "--sequential"]
            self.parser.sequential_command()
            mock_stderr.write.assert_called_once()

    # def test_list_command(self):
    #     # Test list command
    #     with patch('os.walk') as mock_walk:
    #         mock_walk.return_value = [('/path/to/dir', [], ['file1.wav', 'file2.mp3', 'file3.ogg'])]
    #         with patch('builtins.print') as mock_print:
    #             self.parser.list_command()
    #             mock_print.assert_has_calls([
    #                 call('/path/to/dir/file1.wav'),
    #                 call('/path/to/dir/file2.mp3'),
    #                 call('/path/to/dir/file3.ogg')
    #             ])

    def test_rename_command(self):
        # Test rename command with valid arguments
        with patch("os.rename") as mock_rename:
            self.parser.argv = ["", "", "--rename", "old_name.wav", "new_name.wav"]
            self.parser.rename_command()
            mock_rename.assert_called_once_with("old_name.wav", "new_name.wav")

        # Test rename command with missing arguments
        with patch("sys.stderr") as mock_stderr:
            self.parser.argv = ["", "", "--rename"]
            self.parser.rename_command()
            mock_stderr.write.assert_called_once()

    def test_transcode_command(self):
        # Test transcode command
        # test with sounds/coffee.wav and sounds/coffee.mp3
        with patch("saturn_cli.AudioSegment") as mock_audio_segment:
            with patch("saturn_cli.playback.play") as mock_play:
                self.parser.argv = [
                    "",
                    "",
                    "--transcode",
                    "sounds/coffee.wav",
                    "sounds/coffee.mp3",
                ]
                self.parser.transcode_command()
                mock_audio_segment.from_file.assert_called_once_with(
                    "sounds/coffee.mp3", format="mp3"
                )
                mock_play.assert_called_once()
        # then check whether the file is created, and playable
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            with patch("saturn_cli.sa.WaveObject") as mock_wave_obj:
                with patch("saturn_cli.playback.play") as mock_play:
                    self.parser.argv = [
                        "",
                        "",
                        "--transcode",
                        "sounds/coffee.mp3",
                        "sounds/coffee.wav",
                    ]
                    self.parser.transcode_command()
                    mock_wave_obj.from_wave_file.assert_called_once_with(
                        "sounds/coffee.wav"
                    )
                    mock_play.assert_called_once()


if __name__ == "__main__":
    unittest.main()
