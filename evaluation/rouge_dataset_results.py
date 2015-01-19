

class RougeDatasetResults(object):
    """ Class for storing the results of the ROUGE evaluation for multiple texts.
    """

    def __init__(self):
        self.runs = 0
        self.successes = 0
        self.timeouts = 0
        self.errors = 0
        self.reports = []

    def add_success(self, report):
        self.runs += 1
        self.successes += 1
        self.reports.append(report)

    def add_error(self):
        self.runs += 1
        self.errors += 1

    def add_timeout(self):
        self.runs += 1
        self.timeouts += 1