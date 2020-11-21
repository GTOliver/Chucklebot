import random

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
        if msg.type_ in ["ATTACK", "SUPPORT", "WAIT", "RETREAT"]:
            self._latest_suggestion = msg

    def get_action(self):
        response = self._from_suggestion(self._latest_suggestion)
        self._latest_suggestion = None
        return response

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


class CautiousBehaviour(AllyBehaviour):
    def __init__(self, ally):
        super().__init__(ally)
        self._suggestions = {}
        self._support_target = None
        self._zero_suggestions()

    def _zero_suggestions(self):
        self._suggestions = {
            "ATTACK": 0,
            "WAIT": 0,
            "RETREAT": 0,
            "SUPPORT": 0
        }
        self._support_target = None

    def send_message(self, msg):
        if msg.type_ not in ["REBUKE", "PRAISE"]:
            self._suggestions[msg.type_] += 1
        if msg.type_ == "SUPPORT":
            self._support_target = msg.target

    def get_action(self):
        if self._suggestions["RETREAT"] > 0:
            result = ally_actions.retreat()
        else:
            self._suggestions["RETREAT"] = 1
            options = []
            for key, val in self._suggestions.items():
                for i in range(val):
                    options.append(key)
            chosen_action = options[random.randint(0, len(options)-1)]
            if chosen_action == "ATTACK":
                result = ally_actions.attack()
            elif chosen_action == "RETREAT":
                result = ally_actions.retreat()
            elif chosen_action == "WAIT":
                result = ally_actions.wait()
            elif chosen_action == "SUPPORT":
                result = ally_actions.support(self._support_target)
            else:
                result = None
        self._zero_suggestions()
        return result


ALLY_BEHAVIOUR = {
    "default": AllyBehaviour,
    "compliant": CompliantBehaviour,
    "cautious": CautiousBehaviour,
}

