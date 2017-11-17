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

        self.assertEquals(generated_summary, summary)

    def test_reference_text_summarization_with_split(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Makes a summary of the text as a list.
        generated_summary = summarize(text, split=True)

        # To be compared to the method reference.
        summary = get_text_from_test_data("mihalcea_tarau.summ.txt")
        summary = summary.split("\n")

        self.assertSequenceEqual(generated_summary, summary)

    def test_few_distinct_words_summarization_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEquals(summarize(text), "")

    def test_few_distinct_words_summarization_with_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEquals(summarize(text, split=True), [])

    def test_summary_from_unrelated_sentences_is_not_empty_string(self):
        # Tests that the summarization of a text with unrelated sentences is not empty string.
        text = get_text_from_test_data("unrelated.txt")
        self.assertNotEquals(summarize(text), u"")

    def test_summary_from_unrelated_sentences_and_split_is_not_empty_list(self):
        # Tests that the summarization of a text with unrelated sentences is not empty string.
        text = get_text_from_test_data("unrelated.txt")
        self.assertNotEquals(summarize(text, split=True), [])

    def test_text_summarization_on_short_input_text_is_not_empty_string(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEquals(summarize(text), u"")

    def test_text_summarization_on_short_input_text_with_split_is_not_empty_list(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEquals(summarize(text, split=True), [])

    def test_text_summarization_on_single_input_sentence_is_empty_string(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first sentence only.
        text = text.split('\n')[0]

        self.assertEquals(summarize(text), "")

    def test_text_summarization_on_single_input_sentence_with_split_is_empty_list(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first sentence only.
        text = text.split('\n')[0]

        self.assertEquals(summarize(text, split=True), [])

    def test_empty_text_summarization_is_empty_string(self):
        self.assertEquals(summarize(""), u"")

    def test_empty_text_summarization_with_split_is_empty_list(self):
        self.assertEquals(summarize("", split=True), [])

    def test_corpus_summarization_ratio(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        sentences = text.split('\n')

        # Makes summaries of the text using different ratio parameters.
        for x in range(1, 10):
            ratio = x / float(10)
            selected_sentences = summarize(text, ratio=ratio, split=True)
            expected_summary_length = int(len(sentences) * ratio)

            self.assertEqual(len(selected_sentences), expected_summary_length)


if __name__ == '__main__':
    unittest.main()