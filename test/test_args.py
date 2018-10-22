import unittest

from summa.textrank import parse_args, SENTENCE, WORD, DEFAULT_RATIO


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

    def test_ratio_default(self):
        args = parse_args(["-t", "some_text"])
        self.assertEqual(DEFAULT_RATIO, args.ratio)

    def test_ratio_must_be_positive(self):
        with self.assertRaises(SystemExit):
            parse_args(["-t", "some_text", "-r", "-1.0"])

    def test_ratio_must_be_less_than_1(self):
        with self.assertRaises(SystemExit):
            parse_args(["-t", "some_text", "-r", "1.1"])

    def test_words_parameter_short(self):
        args = parse_args(["-t", "some_text", "-w", "200"])
        self.assertEqual(200, args.words)

    def test_words_parameter_long(self):
        args = parse_args(["-t", "some_text", "--words", "200"])
        self.assertEqual(200, args.words)

    def test_additional_stopwords_short(self):
        args = parse_args(["-t", "some_text", "-a", "uno dos tres catorce"])
        self.assertEqual("uno dos tres catorce", args.additional_stopwords)

    def test_additional_stopwords_long(self):
        args = parse_args(["-t", "some_text", "--additional_stopwords", "uno dos tres catorce"])
        self.assertEqual("uno dos tres catorce", args.additional_stopwords)
