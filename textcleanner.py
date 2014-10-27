
#from gensim.utils import tokenize
#from gensim.utils import lemmatize

import re

# StopWords from NLTK
STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
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


def get_clean_sentences(text):
	""" 
		Returns a dictionary with the clean sentence as key, and the original sentence 
		as value.
	"""
	sentences = tokenize_sentences(text)
	

	return "foo"


def tokenize_sentences(text): 
	"""
		http://regex101.com/#python para probar regex.
		Esa NO anda en casos de 'hola\nchau' 
	"""
	pattern = re.compile('(\S.+?[.!?\n])(?=\s+|$)')
	for match in pattern.finditer(text):
		yield match.group()

def filter_stopwords(sentences):
		return [[word for word in sentence.lower().split() if word not in STOPWORDS] for sentence in sentences]