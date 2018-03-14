class Race(object):
    name = ""
    listResults = []

    def __init__(self, name):
        self.name = name
        self.listResults = []



    def write(self):
        print(self.name)
        for result in self.listResults:
            print(result)