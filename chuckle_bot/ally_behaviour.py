from chuckle_bot import ally_actions


class AllyBehaviour:
    def __init__(self, ally):
        # AllyBehaviour knows about the ICharacter interface
        self._ally = ally

    def send_message(self, msg):
        pass

    def get_action(self):
        return ally_actions.wait()


class CompliantBehaviour(AllyBehaviour):
    def __init__(self, ally):
        super().__init__(ally)
        self._latest_suggestion = None

    def send_message(self, msg):
        print('Receiving ' + str(msg))
        if msg.type_ in ["ATTACK", "SUPPORT", "WAIT", "RETREAT"]:
            self._latest_suggestion = msg

    def get_action(self):
        print('Doing ' + str(self._latest_suggestion))
        return self._from_suggestion(self._latest_suggestion)

    @staticmethod
    def _from_suggestion(suggestion):
        if suggestion is None:
            return ally_actions.wait()
        if suggestion.type_ == "WAIT":
            return ally_actions.wait()
        if suggestion.type_ == "ATTACK":
            return ally_actions.attack()
        if suggestion.type_ == "RETREAT":
            return ally_actions.retreat()
        if suggestion.type_ == "SUPPORT":
            return ally_actions.support(suggestion.secondary_subject)


class CautiousBehaviour:
    def send_message(self, msg):
        pass

    def get_action(self):
        return ally_actions.wait()


ALLY_BEHAVIOUR = {
    "default": AllyBehaviour,
    "compliant": CompliantBehaviour,
    "cautious": CautiousBehaviour,
}

