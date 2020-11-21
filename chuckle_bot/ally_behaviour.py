from chuckle_bot import ally_actions


class AllyBehaviour:
    def __init__(self, ally):
        # AllyBehaviour knows about the ICharacter interface
        self._ally = ally

    def send_message(self, msg):
        pass

    def get_action(self):
        return ally_actions.attack()
