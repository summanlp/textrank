
from itertools import combinations
from rouge_calculator import MODEL_DIRECTORY
from rouge_calculator import MODEL_FILENAME
from rouge_calculator import TEXT_FILENAME_FORMAT
from rouge_calculator import GOLD_REFERENCES_DIR_FORMAT

SUMMARY_LENGHT = 0.2
DATASET = 'summa'

def get_optimum_summary(text_number):
    """ Creates the best possible summary of a set length trying
    all posible combinations.
    """

    # Temporary stores the best results so far.
    best_sentences = None
    best_scores = None

    
    text_filename = TEXT_FILENAME_FORMAT.format(dataset=DATASET, text_number=text_number)



    gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=DATASET, text_number=text_number)


