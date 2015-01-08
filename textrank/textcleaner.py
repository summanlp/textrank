# encoding: cp850

from gensim.utils import tokenize
from gensim.parsing.preprocessing import strip_numeric, strip_punctuation
import snowball

import re  # http://regex101.com/#python para probar regex.

SEPARATOR = r"@"
RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')  # backup (\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)
AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)\s(\w)")
AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)\s(\w)")
UNDO_AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)" + SEPARATOR + "(\w)")
UNDO_AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)" + SEPARATOR + "(\w)")


# StopWords from NLTK
STOPWORDS = """
all six eleven just less being indeed over both anyway detail four front already through yourselves fify  
mill still its before move whose one system also somewhere herself thick show had enough should to only  
seeming under herein ours two has might thereafter do them his around thereby get very de none cannot  
every whether they not during thus now him nor name regarding several hereafter did always cry whither  
beforehand this someone she each further become thereupon where side towards few twelve because often ten  
anyhow doing km eg some back used go namely besides yet are cant our beyond ourselves sincere out even  
what throughout computer give for bottom mine since please while per find everything behind does various  
above between kg neither seemed ever across t somehow be we who were sixty however here otherwise whereupon  
nowhere although found hers re along quite fifteen by on about didn last would anything via of could thence  
put against keep etc s became ltd hence therein onto or whereafter con among own co afterwards formerly  
within seems into others whatever yourself down alone everyone done least another whoever moreover couldnt  
must your three from her their together top there due been next anyone whom much call too interest thru  
themselves hundred was until empty more himself elsewhere mostly that fire becomes becoming hereby but  
else part everywhere former don with than those he me forty myself made full twenty these bill using up us  
will nevertheless below anywhere nine can theirs toward my something and sometimes whenever sometime then  
almost wherever is describe am it doesn an really as itself at have in seem whence ie any if again hasnt  
inc un thin no perhaps latter meanwhile when amount same wherein beside how other take which latterly you  
fill either nobody unless whereas see though may after upon therefore most hereupon eight amongst never  
serious nothing such why a off whereby third i whole noone many well except amoungst yours rather without  
so five the first having once
"""
STOPWORDS = frozenset(w for w in STOPWORDS.split() if w)


def tokenize_by_sentences(text):
	"""
    Given some text, tokenizes into sentences, applies filters and lemmatizes them.
    Returns dictionary that map processed sentences to the originals sentences.
    """
	original_sentences = split_sentences(text)
	filtered_sentences = filter_words(original_sentences)
	return {item[0]: item[1] for item in zip(filtered_sentences, original_sentences) if item[0]}


def split_sentences(text):
	processed = replace_abbreviations(text)
	return [undo_replacement(sentence) for sentence in get_sentences(processed)]


def replace_abbreviations(text):
	return replace_with_separator(text, SEPARATOR, [AB_SENIOR, AB_ACRONYM])


def undo_replacement(sentence):
	return replace_with_separator(sentence, r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM])


def replace_with_separator(text, separator, regexs):
	replacement = r"\1" + separator + r"\2"
	result = text
	for regex in regexs:
		result = regex.sub(replacement, result)
	return result


def get_sentences(text):
	for match in RE_SENTENCE.finditer(text):
		yield match.group()


def filter_words(tokens):
	filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, remove_stopwords,
			   stem_sentence]
	# filters = []

	apply_filters_to_token = lambda token: apply_filters(token, filters)
	return map(apply_filters_to_token, tokens)


def apply_filters(sentence, filters):
	for f in filters:
		sentence = f(sentence)
	return sentence


def remove_stopwords(sentence):
	return " ".join(w for w in sentence.split() if w not in STOPWORDS)


language = "english"
stemmer = snowball.SnowballStemmer(language)


def stem_sentence(sentence):
	word_stems = [stemmer.stem(word) for word in sentence.split()]
	return " ".join(word_stems)


# Falta bocha por aca:
#  - Corregir bug cuando alguna palabra se transforma a ""
#  - Ver que se debe hacer con las palabras repetidas (releer paper)

def tokenize_by_word(text):
	# pdb.set_trace()
	original_words = list(tokenize(text, to_lower=True))
	return filter_words(original_words)
