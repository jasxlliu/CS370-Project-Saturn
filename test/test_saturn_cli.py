import unittest
import sys
from io import StringIO
from unittest.mock import patch

sys.path.append("src")
from saturn_cli import Saturn, CommandLineParser


class TestSaturn(unittest.TestCase):

    @patch("simpleaudio.WaveObject")
    def test_play_method_wav(self, mock_wave_object):
        saturn = Saturn([], 0)
        saturn.play("test.wav")
        mock_wave_object.from_wave_file.assert_called_once_with("test.wav")

    @patch("pydub.AudioSegment")
    @patch("pydub.playback.play")
    def test_play_method_non_wav(self, mock_play, mock_audio_segment):
        saturn = Saturn([], 0)
        saturn.play("test.mp3")
        mock_audio_segment.from_file.assert_called_once_with("test.mp3", format="mp3")
        mock_play.assert_called_once()

    @patch("pydub.AudioSegment")
    @patch("pydub.playback.play")
    def test_play_overlap(self, mock_play, mock_audio_segment):
        saturn = Saturn([], 0)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            saturn.play_overlap(["test1.wav", "test2.wav"])
            self.assertIn(
                "I am now playing files overlapping each other:", fake_out.getvalue()
            )
        mock_audio_segment.from_file.assert_called()
        self.assertEqual(mock_play.call_count, 2)

    @patch("pydub.AudioSegment")
    @patch("pydub.playback.play")
    def test_play_sequential(self, mock_play, mock_audio_segment):
        saturn = Saturn([], 0)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            saturn.play_sequential(["test1.wav", "test2.wav"])
            self.assertIn("Playing:", fake_out.getvalue())
        mock_audio_segment.from_file.assert_called()
        self.assertEqual(mock_play.call_count, 2)

    @patch("os.walk")
    def test_list_command(self, mock_walk):
        mock_walk.return_value = [("", [], ["test.wav", "test.mp3"])]
        saturn = Saturn([], 0)
        with patch("builtins.print") as mock_print:
            saturn.list_command()
            mock_print.assert_called_with("test.wav")
            mock_print.assert_called_with("test.mp3")

    # Add more tests for other methods as needed


class TestCommandLineParser(unittest.TestCase):

    def test_parse_arguments_help(self):
        with patch("sys.argv", ["script.py", "--help"]):
            with self.assertRaises(SystemExit) as cm:
                CommandLineParser(sys.argv)
            self.assertEqual(cm.exception.code, 0)

    def test_parse_arguments_invalid_command(self):
        with patch("sys.argv", ["script.py", "invalid_command"]):
            with patch("sys.stderr", new=StringIO()) as fake_err:
                with self.assertRaises(SystemExit) as cm:
                    CommandLineParser(sys.argv)
                self.assertEqual(cm.exception.code, 1)
                self.assertIn("error, unexpected arguments", fake_err.getvalue())

    # Add more tests for other commands as needed


if __name__ == "__main__":
    unittest.main()
