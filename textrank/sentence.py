
class Sentence(object):

    def __init__(self):
        self.index = -1
        self.text = None
        self.tokens = None
        self.score = -1

    def __str__(self):
        return "Original sentence: " + self.text + "\n" + "Processed sentence: " + self.tokens
