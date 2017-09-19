import unittest

from summa.summarizer import summarize
from utils import get_text_from_test_data


class TestSummarizer(unittest.TestCase):

    def test_reference_text_summarization(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Makes a summary of the text.
        generated_summary = summarize(text)

        # To be compared to the method reference.
        summary = get_text_from_test_data("mihalcea_tarau.summ.txt")

        self.assertEqual(generated_summary, summary)


if __name__ == '__main__':
    unittest.main()