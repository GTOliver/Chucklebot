class AllyVocabulary:
    def __init__(self, ally):
        # Uses the ICharacter interface
        self._ally = ally

    def announce_action(self, action):
        """ Get a text version of the action """
        return action.type_
