import luigi

class Dummy1(luigi.Task):
    has_been_run = False

    def run(self):
        self.has_been_run = True

    def complete(self):
        if self.has_been_run:
            return True
        return False

class Dummy2(Dummy1):
    has_been_run = False
    def requires(self):
        yield Dummy1()
