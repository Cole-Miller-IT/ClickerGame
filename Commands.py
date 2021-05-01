class Command():
    def __init__(self):
        pass

    def run(self):
        pass

class MoveCommand(Command):
    def __init__(self, state, entity, move):
        self.state = state
        self.entity = entity
        self.move = move

    def run(self):
        pass