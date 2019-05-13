import unittest

from summa.keywords import keywords
from summa.preprocessing.textcleaner import deaccent
from numpy import isclose
from .utils import get_text_from_test_data


class TestKeywords(unittest.TestCase):

    def test_text_keywords(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Calculate keywords
        generated_keywords = keywords(text, split=True)

        # To be compared to the reference.
        reference_keywords = get_text_from_test_data("mihalcea_tarau.kw.txt").split("\n")

        self.assertEqual({str(x) for x in generated_keywords}, {str(x) for x in reference_keywords})

    def test_text_keywords_wempty_stoplist(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")
        additional_stoplist = []
        generated_keywords = keywords(text, split=True, additional_stopwords=additional_stoplist)
        reference_keywords = get_text_from_test_data("mihalcea_tarau.kw.txt").split("\n")
        self.assertEqual({str(x) for x in generated_keywords}, {str(x) for x in reference_keywords})

    def test_text_keywords_wstoplist(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")
        additional_stoplist = get_text_from_test_data("mihalcea_tarau.sw.txt").strip().split(",")
        generated_keywords = keywords(text, split=True, additional_stopwords=additional_stoplist)
        reference_keywords = get_text_from_test_data("mihalcea_tarau.swkw.txt").split("\n")
        self.assertEqual({str(x) for x in generated_keywords}, {str(x) for x in reference_keywords})

    def test_keywords_few_distinct_words_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEqual(keywords(text), "")

    def test_keywords_few_distinct_words_wempty_stoplist_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEqual(keywords(text,additional_stopwords=[]), "")

    def test_keywords_few_distinct_words_w_stoplist_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        additional_stopwords = ["here","there"]
        self.assertEqual(keywords(text,additional_stopwords=additional_stopwords), "")

    def test_keywords_few_distinct_words_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEqual(keywords(text, split=True), [])

    def test_keywords_few_distinct_words_wempty_stoplist_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEqual(keywords(text, split=True, additional_stopwords=[]), [])

    def test_keywords_few_distinct_words_w_stoplist_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        additional_stopwords = ["here","there"]
        self.assertEqual(keywords(text, split=True, additional_stopwords=additional_stopwords), [])

    def test_text_summarization_on_short_input_text_and_split_is_not_empty_list(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEqual(keywords(text, split=True), [])

    def test_text_summarization_on_short_input_text_is_not_empty_string(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEqual(keywords(text, split=True), "")

    def test_keywords_ratio(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Check ratio parameter is well behaved.
        # Because length is taken on tokenized clean text we just check that
        # ratio 40% is twice as long as ratio 20%
        selected_docs_20 = keywords(text, ratio=0.2, split=True)
        selected_docs_40 = keywords(text, ratio=0.4, split=True)

        self.assertAlmostEqual(float(len(selected_docs_40)) / len(selected_docs_20), 0.4 / 0.2, places=1)

    def test_keywords_ratio_wstopwords(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")
        additional_stoplist = get_text_from_test_data("mihalcea_tarau.sw.txt").strip().split(",")
        # Check ratio parameter is well behaved.
        # Because length is taken on tokenized clean text we just check that
        # ratio 40% is twice as long as ratio 20%
        selected_docs_20 = keywords(text, ratio=0.2, split=True, additional_stopwords=additional_stoplist)
        selected_docs_40 = keywords(text, ratio=0.4, split=True, additional_stopwords=additional_stoplist)

        actual_ratio = float(len(selected_docs_40)) / len(selected_docs_20)
        expected_ratio = 0.4 / 0.2
        # Expect the same ratio with a relative tolerance of 5%.
        self.assertTrue(isclose(actual_ratio, expected_ratio, rtol=0.5), "Ratio between number of keywords should be 2.")

    def test_keywords_consecutive_keywords(self):
        text = "Rabbit populations known to be plentiful, large, and diverse \
                in the area. \
                Adjacent to the site, a number number well over a thousand. \
                The number of these rabbit populations has diminished in recent \
                years, and perhaps we have become number to a number of their \
                numbers numbering fewer."

        # Should not raise an exception.
        self.assertIsNotNone(keywords(text, words=10))

    def test_repeated_keywords(self):
        text = get_text_from_test_data("repeated_keywords.txt")
        kwds = keywords(text)
        self.assertTrue(len(kwds.splitlines()))

    def test_repeated_keywords_wstopwords(self):
        text = get_text_from_test_data("repeated_keywords.txt")
        additional_stoplist = ["sage","user"]
        kwds = keywords(text,additional_stopwords=additional_stoplist)
        self.assertTrue(len(kwds.splitlines()))

    def test_spanish_without_accents(self):
        # Test the keyword extraction with accented characters.
        text = get_text_from_test_data("spanish.txt")
        kwds = keywords(text, language="spanish", deaccent=True, split=True)
        # Verifies that all words are retrieved without accents.
        self.assertTrue(all(deaccent(keyword) == keyword for keyword in kwds))

    def test_spanish_with_accents(self):
        # Test the keyword extraction with accented characters.
        text = get_text_from_test_data("spanish.txt")
        kwds = keywords(text, language="spanish", deaccent=False, split=True)
        # Verifies that there are some keywords are retrieved with accents.
        self.assertTrue(any(deaccent(keyword) != keyword for keyword in kwds))

    def test_text_as_bytes_raises_exception(self):
        # Test the keyword extraction for a text that is not a unicode object
        # (Python 3 str).
        text = get_text_from_test_data("spanish.txt")
        bytes = text.encode(encoding="utf-8")
        with self.assertRaises(ValueError):
            keywords(bytes, language="spanish")


if __name__ == '__main__':
    unittest.main()