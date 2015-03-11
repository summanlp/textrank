
class SyntacticUnit(object):

    def __init__(self, text, token=None, tag=None):
        self.text = text
        self.token = token
        if tag:
            self.tag = tag[:2] # just first two letters of tag
        self.index = -1
        self.score = -1

    def __str__(self):
        return "Original unit: '" + self.text + "' *-*-*-* " + "Processed unit: '" + self.token + "'"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.token)

    def __eq__(self, other):
        return isinstance(other, SyntacticUnit) and hash(self) == hash(other)