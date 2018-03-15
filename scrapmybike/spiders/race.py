class Race(object):
    name = ""
    listResults = []

    def __init__(self, name):
        self.name = name
        self.listResults = []

    def getResult(self, rider):
        result = filter(lambda x: x[1].startswith(rider), self.listResults)
        if len(result) == 0:
            return '0'
        else:
            return str(result[0][0])

    def write(self):
        print(self.name)
        for result in self.listResults:
            print(result)