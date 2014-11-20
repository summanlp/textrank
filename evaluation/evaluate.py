import os
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from pyrouge import Rouge155
from textrank.textrank import textrank

ROUGE_PATH = os.path.join(os.getcwd(), 'ROUGE-RELEASE-1.5.5')
Rouge155(ROUGE_PATH)

with open('datasets/cmplg/001/text.txt') as fp:
    text = fp.read()

summary = textrank(text)

with open('temp.txt', 'w') as fp:
    fp.write(summary)

