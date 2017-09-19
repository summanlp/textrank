import unittest

from summa.keywords import keywords
from utils import get_text_from_test_data


class TestSummarizer(unittest.TestCase):

    def test_keywords(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        kwds = keywords(text)
        self.assertTrue(len(kwds.splitlines()))

        kwds_u = keywords(unicode(text))
        self.assertTrue(len(kwds_u.splitlines()))

        kwds_lst = keywords(text, split=True)
        self.assertTrue(len(kwds_lst))

    def test_keywords_few_distinct_words_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEquals(keywords(text), "")

    def test_keywords_few_distinct_words_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEquals(keywords(text, split=True), [])

if __name__ == '__main__':
    unittest.main()