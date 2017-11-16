import unittest

from summa.keywords import keywords
from utils import get_text_from_test_data


class TestKeywords(unittest.TestCase):

    def test_keywords_few_distinct_words_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEquals(keywords(text), "")

    def test_keywords_few_distinct_words_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEquals(keywords(text, split=True), [])

    def test_text_summarization_on_short_input_text_and_split_is_not_empty_list(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEquals(keywords(text, split=True), [])

    def test_text_summarization_on_short_input_text_is_not_empty_string(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEquals(keywords(text, split=True), "")

    def test_keywords_ratio(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Check ratio parameter is well behaved.
        # Because length is taken on tokenized clean text we just check that
        # ratio 40% is twice as long as ratio 20%
        selected_docs_20 = keywords(text, ratio=0.2, split=True)
        selected_docs_40 = keywords(text, ratio=0.4, split=True)

        self.assertAlmostEqual(float(len(selected_docs_40)) / len(selected_docs_20), 0.4 / 0.2, places=1)


if __name__ == '__main__':
    unittest.main()