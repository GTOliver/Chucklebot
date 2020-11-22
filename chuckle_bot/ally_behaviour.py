import random

from chuckle_bot import ally_actions


class AllyBehaviour:
    def send_message(self, msg):
        pass

    def get_action(self):
        return ally_actions.wait()

    @staticmethod
    def _perform(action, target=None):
        if action == "WAIT":
            return ally_actions.wait()
        if action == "ATTACK":
            return ally_actions.attack()
        if action == "RETREAT":
            return ally_actions.retreat()
        if action == "SUPPORT":
            return ally_actions.support(target)

    def reset(self):
        pass


class CompliantBehaviour(AllyBehaviour):
    def __init__(self):
        super().__init__()
        self._latest_suggestion = None

    def send_message(self, msg):
        if msg.type_ in ["ATTACK", "SUPPORT", "WAIT", "RETREAT"]:
            self._latest_suggestion = msg

    def get_action(self):
        response = self._from_suggestion(self._latest_suggestion)
        self._latest_suggestion = None
        return response

    def reset(self):
        self._latest_suggestion = None

    @staticmethod
    def _from_suggestion(suggestion):
        if suggestion is None:
            return ally_actions.wait()
        return AllyBehaviour._perform(suggestion.type_, suggestion.secondary_subject)


class BiasedActionBehaviour(AllyBehaviour):
    """ Has a preferred action.

        Always has a chance of doing that action.
        If that action has been suggested, will always do it.
    """
    def __init__(self, preferred_action):
        super().__init__()
        self._bias = preferred_action
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
        if self._suggestions[self._bias] > 0:
            result = AllyBehaviour._perform(self._bias, self._support_target)
        else:
            self._suggestions[self._bias] = 1
            options = []
            for key, val in self._suggestions.items():
                for i in range(val):
                    options.append(key)
            chosen_action = options[random.randint(0, len(options)-1)]
            result = AllyBehaviour._perform(chosen_action, self._support_target)
        self._zero_suggestions()
        return result

    def reset(self):
        self._zero_suggestions()
        super().reset()


class CautiousBehaviour(BiasedActionBehaviour):
    def __init__(self):
        super().__init__("RETREAT")


class AggressiveBehaviour(BiasedActionBehaviour):
    def __init__(self):
        super().__init__("ATTACK")


class DocileBehaviour(BiasedActionBehaviour):
    def __init__(self):
        super().__init__("WAIT")


ALLY_BEHAVIOUR = {
    "idle": AllyBehaviour,
    "compliant": CompliantBehaviour,
    "cautious": CautiousBehaviour,
    "aggressive": AggressiveBehaviour,
    "docile": DocileBehaviour
}

