import unittest
from summa.textrank import parse_args, SENTENCE, WORD, DEFAULT_RATIO
from test.utils import get_test_file_path, silence_stderr


class TestArgs(unittest.TestCase):

    @silence_stderr
    def test_parse_fails_with_no_options(self):
        with self.assertRaises(SystemExit):
            parse_args([])

    @silence_stderr
    def test_parse_fails_with_no_text_option_summarize(self):
        with self.assertRaises(SystemExit):
            parse_args(["--summarize"])

    @silence_stderr
    def test_parse_fails_with_no_text_option_keywords(self):
        with self.assertRaises(SystemExit):
            parse_args(["--keywords"])

    @silence_stderr
    def test_parse_fails_if_multiple_modes_selected(self):
        with self.assertRaises(SystemExit):
            parse_args(["--summarize", get_test_file_path("mihalcea_tarau.txt"),
                        "-t", get_test_file_path("mihalcea_tarau.txt")])

    @silence_stderr
    def test_parse_fails_with_no_text_short(self):
        with self.assertRaises(SystemExit):
            parse_args(["-t"])

    @silence_stderr
    def test_parse_fails_with_no_text_long(self):
        with self.assertRaises(SystemExit):
            parse_args(["--text"])

    def test_parse_text_summarize(self):
        args = parse_args(["--summarize", get_test_file_path("mihalcea_tarau.txt")])
        self.assertTrue(isinstance(args.summarize, str))

    def test_parse_text_keywords(self):
        args = parse_args(["--keywords", get_test_file_path("mihalcea_tarau.txt")])
        self.assertTrue(isinstance(args.keywords, str))

    def test_parse_text_short(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt")])
        self.assertTrue(isinstance(args.text, str))

    def test_parse_text_long(self):
        args = parse_args(["--text", get_test_file_path("mihalcea_tarau.txt")])
        self.assertTrue(isinstance(args.text, str))

    def test_summary_mode_is_default(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt")])
        self.assertEqual(SENTENCE, args.summary)

    def test_summary_mode_can_be_overriden(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "-s", str(SENTENCE)])
        self.assertEqual(SENTENCE, args.summary)

    def test_keyword_mode(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "-s", str(WORD)])
        self.assertEqual(WORD, args.summary)

    def test_ratio_default(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt")])
        self.assertEqual(DEFAULT_RATIO, args.ratio)

    @silence_stderr
    def test_ratio_must_be_positive(self):
        with self.assertRaises(SystemExit):
            parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "-r", "-1.0"])

    @silence_stderr
    def test_ratio_must_be_less_than_1(self):
        with self.assertRaises(SystemExit):
            parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "-r", "1.1"])

    def test_words_parameter_short(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "-w", "200"])
        self.assertEqual(200, args.words)

    def test_words_parameter_long(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "--words", "200"])
        self.assertEqual(200, args.words)

    def test_additional_stopwords_short(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "-a", "uno dos tres catorce"])
        self.assertEqual("uno dos tres catorce", args.additional_stopwords)

    def test_additional_stopwords_long(self):
        args = parse_args(["-t", get_test_file_path("mihalcea_tarau.txt"), "--additional_stopwords", "uno dos tres catorce"])
        self.assertEqual("uno dos tres catorce", args.additional_stopwords)
