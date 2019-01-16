import unittest

from summa.summarizer import summarize
from .utils import get_text_from_test_data


class TestSummarizer(unittest.TestCase):

    def test_reference_text_summarization(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Makes a summary of the text.
        generated_summary = summarize(text)

        # To be compared to the method reference.
        summary = get_text_from_test_data("mihalcea_tarau.summ.txt")

        self.assertEqual(generated_summary, summary)

    def test_reference_text_summarization_wstopwords(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")
        additional_stoplist = get_text_from_test_data("mihalcea_tarau.sw.txt").strip().split(",")
        # Makes a summary of the text.
        generated_summary = summarize(text,additional_stopwords=additional_stoplist)

        # To be compared to the method reference.
        summary = get_text_from_test_data("mihalcea_tarau.summ.txt")

        self.assertEqual(generated_summary, summary)

    def test_reference_text_summarization_with_split(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        # Makes a summary of the text as a list.
        generated_summary = summarize(text, split=True)

        # To be compared to the method reference.
        summary = get_text_from_test_data("mihalcea_tarau.summ.txt")
        summary = summary.split("\n")

        self.assertSequenceEqual(generated_summary, summary)

    def test_reference_text_summarization_wstopwords_with_split(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")
        additional_stoplist = get_text_from_test_data("mihalcea_tarau.sw.txt").strip().split(",")

        # Makes a summary of the text as a list.
        generated_summary = summarize(text, split=True, additional_stopwords=additional_stoplist)

        # To be compared to the method reference.
        summary = get_text_from_test_data("mihalcea_tarau.summ.txt")
        summary = summary.split("\n")

        self.assertSequenceEqual(generated_summary, summary)

    def test_few_distinct_words_summarization_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEqual(summarize(text), "")

    def test_few_distinct_words_summarization_with_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        self.assertEqual(summarize(text, split=True), [])

    def test_few_distinct_words_summarization_wstopwords_is_empty_string(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        additional_stoplist = ["here","there"]
        self.assertEqual(summarize(text, additional_stopwords=additional_stoplist), "")

    def test_few_distinct_words_summarization_wstopwords_with_split_is_empty_list(self):
        text = get_text_from_test_data("few_distinct_words.txt")
        additional_stoplist = ["here","there"]
        self.assertEqual(summarize(text, split=True, additional_stopwords=additional_stoplist), [])

    def test_summary_from_unrelated_sentences_is_not_empty_string(self):
        # Tests that the summarization of a text with unrelated sentences is not empty string.
        text = get_text_from_test_data("unrelated.txt")
        self.assertNotEqual(summarize(text), "")

    def test_summary_from_unrelated_sentences_and_split_is_not_empty_list(self):
        # Tests that the summarization of a text with unrelated sentences is not empty string.
        text = get_text_from_test_data("unrelated.txt")
        self.assertNotEqual(summarize(text, split=True), [])

    def test_text_summarization_on_short_input_text_is_not_empty_string(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEqual(summarize(text), "")

    def test_text_summarization_on_short_input_text_with_split_is_not_empty_list(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first 8 sentences to make the text shorter.
        text = "\n".join(text.split('\n')[:8])

        self.assertNotEqual(summarize(text, split=True), [])

    def test_text_summarization_on_single_input_sentence_is_empty_string(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first sentence only.
        text = text.split('\n')[0]

        self.assertEqual(summarize(text), "")

    def test_text_summarization_on_single_input_sentence_with_split_is_empty_list(self):
        text = get_text_from_test_data("unrelated.txt")

        # Keeps the first sentence only.
        text = text.split('\n')[0]

        self.assertEqual(summarize(text, split=True), [])

    def test_empty_text_summarization_is_empty_string(self):
        self.assertEqual(summarize(""), "")

    def test_empty_text_summarization_with_split_is_empty_list(self):
        self.assertEqual(summarize("", split=True), [])

    def test_corpus_summarization_ratio(self):
        text = get_text_from_test_data("mihalcea_tarau.txt")

        sentences = text.split('\n')

        # Makes summaries of the text using different ratio parameters.
        for x in range(1, 10):
            ratio = x / float(10)
            selected_sentences = summarize(text, ratio=ratio, split=True)
            expected_summary_length = int(len(sentences) * ratio)

            self.assertEqual(len(selected_sentences), expected_summary_length)

    def test_spanish(self):
        # Test the summarization module with accented characters.
        text = get_text_from_test_data("spanish.txt")
        self.assertIsNotNone(summarize(text, language="spanish"))

    def test_polish(self):
        # Test the summarization module for Polish language.
        text = get_text_from_test_data("polish.txt")
        self.assertIsNotNone(summarize(text, language="polish"))

    def test_text_as_bytes_raises_exception(self):
        # Test the keyword extraction for a text that is not a unicode object
        # (Python 3 str).
        text = get_text_from_test_data("spanish.txt")
        bytes = text.encode(encoding="utf-8")
        with self.assertRaises(ValueError):
            summarize(bytes, language="spanish")
    
    def test_arabic(self):
         # Test the summarization module for arabic language.
        text = get_text_from_test_data("arabic.txt")
        self.assertIsNotNone(summarize(text, language='arabic'))


if __name__ == '__main__':
    unittest.main()