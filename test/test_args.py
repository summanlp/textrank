import unittest

from summa.textrank import parse_args


class TestArgs(unittest.TestCase):

    def test_parse_fails_with_no_text(self):
        with self.assertRaises(SystemExit):
            parse_args([])

    def test_parse_doesnt_fail_with_text_short(self):
        args = parse_args(["-t", "some_text"])
        self.assertEquals("some_text", args.text)

    def test_parse_doesnt_fail_with_text_long(self):
        args = parse_args(["--text", "some_text"])
        self.assertEquals("some_text", args.text)
