# encoding: cp850

import string
import unicodedata
import logging
logger = logging.getLogger('summa.preprocessing.cleaner')

try:
    from pattern.en import tag
    logger.info("'pattern' package found; tag filters are available for English")
    HAS_PATTERN = True
except ImportError:
    logger.info("'pattern' package not found; tag filters are not available for English")
    HAS_PATTERN = False

from snowball import SnowballStemmer
import re  # http://regex101.com/#python to test regex
from summa.syntactic_unit import SyntacticUnit

SEPARATOR = r"@"
RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')  # backup (\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)
AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)\s(\w)")
AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)\s(\w)")
AB_ACRONYM_LETTERS = re.compile("([a-zA-Z])\.([a-zA-Z])\.")
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

LANGUAGES = {"EN": "english"}
STEMMER = None


def set_stemmer_language(language):
    global STEMMER
    if not language in LANGUAGES:
        raise ValueError("Valid languages are danish, dutch, english, finnish," +
                 " french, german, hungarian, italian, norwegian, porter, portuguese," +
                 "romanian, russian, spanish, swedish")
    stemmer_language = LANGUAGES[language]
    STEMMER = SnowballStemmer(stemmer_language)


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


# Taken from gensim
def to_unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)


# Taken from gensim
RE_PUNCT = re.compile('([%s])+' % re.escape(string.punctuation), re.UNICODE)
def strip_punctuation(s):
    s = to_unicode(s)
    return RE_PUNCT.sub(" ", s)


# Taken from gensim
RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)
def strip_numeric(s):
    s = to_unicode(s)
    return RE_NUMERIC.sub("", s)


def remove_stopwords(sentence):
    return " ".join(w for w in sentence.split() if w not in STOPWORDS)


def stem_sentence(sentence):
    word_stems = [STEMMER.stem(word) for word in sentence.split()]
    return " ".join(word_stems)


def apply_filters(sentence, filters):
    for f in filters:
        sentence = f(sentence)
    return sentence


def filter_words(sentences):
    filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, #remove_stopwords,
               stem_sentence]
    # filters = []

    apply_filters_to_token = lambda token: apply_filters(token, filters)
    return map(apply_filters_to_token, sentences)


# Taken from six
def u(s):
    return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")


# Taken from gensim
def deaccent(text):
    """
    Remove accentuation from the given string. Input text is either a unicode string or utf8
    encoded bytestring.
    """
    if not isinstance(text, unicode):
        # assume utf8 for byte strings, use default (strict) error handling
        text = text.decode('utf8')
    norm = unicodedata.normalize("NFD", text)
    result = u('').join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize("NFC", result)


# Taken from gensim
PAT_ALPHABETIC = re.compile('(((?![\d])\w)+)', re.UNICODE)
def tokenize(text, lowercase=False, deacc=False, errors="strict", to_lower=False, lower=False):
    """
    Iteratively yield tokens as unicode strings, optionally also lowercasing them
    and removing accent marks.
    """
    lowercase = lowercase or to_lower or lower
    text = to_unicode(text, errors=errors)
    if lowercase:
        text = text.lower()
    if deacc:
        text = deaccent(text)
    for match in PAT_ALPHABETIC.finditer(text):
        yield match.group()


def merge_syntactic_units(original_units, filtered_units, tags=None):
    units = []
    for i in xrange(len(original_units)):
        if filtered_units[i] == '':
            continue

        text = original_units[i]
        token = filtered_units[i]
        tag = tags[i][1] if tags else None
        sentence = SyntacticUnit(text, token, tag)
        sentence.index = i

        units.append(sentence)

    return units


def clean_text_by_sentences(text, language="EN"):
    """ Tokenizes a given text into sentences, applying filters and lemmatizing them.
    Returns a SyntacticUnit list. """
    set_stemmer_language(language)
    original_sentences = split_sentences(text)
    filtered_sentences = filter_words(original_sentences)

    return merge_syntactic_units(original_sentences, filtered_sentences)


def clean_text_by_word(text, language="EN"):
    """ Tokenizes a given text into words, applying filters and lemmatizing them.
    Returns a dict of word -> syntacticUnit. """
    set_stemmer_language(language)
    text_without_acronyms = replace_with_separator(text, "", [AB_ACRONYM_LETTERS])
    original_words = list(tokenize(text_without_acronyms, to_lower=True, deacc=True))
    filtered_words = filter_words(original_words)
    if HAS_PATTERN:
        tags = tag(" ".join(original_words)) # tag needs the context of the words in the text
    else:
        tags = None
    units = merge_syntactic_units(original_words, filtered_words, tags)
    return { unit.text : unit for unit in units }


def tokenize_by_word(text):
    text_without_acronyms = replace_with_separator(text, "", [AB_ACRONYM_LETTERS])
    return tokenize(text_without_acronyms, to_lower=True, deacc=True)
