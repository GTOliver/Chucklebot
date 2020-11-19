class AllyBehaviour:
    def __init__(self, ally):
        # AllyBehaviour knows about the ICharacter interface
        self._ally = ally

    def send_message(self, msg):
        pass

    def take_turn(self):
        return "My name is " + self._ally.name
