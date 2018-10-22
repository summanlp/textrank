import unittest

from summa.textrank import parse_args, SENTENCE, WORD


class TestArgs(unittest.TestCase):

    def test_parse_fails_with_no_text_option(self):
        with self.assertRaises(SystemExit):
            parse_args([])

    def test_parse_fails_with_no_text_short(self):
        with self.assertRaises(SystemExit):
            parse_args(["-t"])

    def test_parse_fails_with_no_text_long(self):
        with self.assertRaises(SystemExit):
            parse_args(["--text"])

    def test_parse_text_short(self):
        args = parse_args(["-t", "some_text"])
        self.assertEqual("some_text", args.text)

    def test_parse_text_long(self):
        args = parse_args(["--text", "some_text"])
        self.assertEqual("some_text", args.text)

    def test_summary_mode_is_default(self):
        args = parse_args(["-t", "some_text"])
        self.assertEqual(SENTENCE, args.summary)

    def test_summary_mode_can_be_overriden(self):
        args = parse_args(["-t", "some_text", "-s", str(SENTENCE)])
        self.assertEqual(SENTENCE, args.summary)

    def test_keyword_mode(self):
        args = parse_args(["-t", "some_text", "-s", str(WORD)])
        self.assertEqual(WORD, args.summary)
