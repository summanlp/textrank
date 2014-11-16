import os
import os.path

from pyrouge import Rouge155

ROUGE_PATH = os.path.join(os.getcwd(), 'ROUGE-RELEASE-1.5.5')
Rouge155(ROUGE_PATH)

from pyrouge import test