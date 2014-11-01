
#from gensim.utils import tokenize
#from gensim.utils import lemmatize

import re

SEPARATOR = r"@"
AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)\s(\w)")
AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)\s(\w)")
UNDO_AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)" + SEPARATOR + "(\w)")
UNDO_AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)" + SEPARATOR + "(\w)")


# StopWords from NLTK
STOPWORDS = frozenset(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])


def get_tokenized_sentences(text):
	""" 
		Returns a dictionary with the clean sentence as key, and the original sentence 
		as value.
	"""
	processed = replace_abbreviations(text)
	return process_text(processed)

def replace_abbreviations(text):
	return replace_with_separator(text, SEPARATOR, [AB_SENIOR, AB_ACRONYM])

def replace_with_separator(text, separator, regexs):
	replacement = r"\1" + separator + r"\2"
	result = text
	for regex in regexs:
		result = regex.sub(replacement, result)
	return result


def process_text(text):
	result = []
	for sentence in tokenize_sentences(text):
		result.append(undo_replacement(sentence))
	return result


def tokenize_sentences(text): 
	"""
		http://regex101.com/#python para probar regex.
		Esa NO anda en casos de 'hola\nchau' 
	"""
	pattern = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?\n)')
	for match in pattern.finditer(text):
		yield match.group()


def undo_replacement(sentence):
	return replace_with_separator(sentence, r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM])


def filter_stopwords(sentences):
		return [[word for word in sentence.lower().split() if word not in STOPWORDS] for sentence in sentences]