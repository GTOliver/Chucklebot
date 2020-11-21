from chuckle_bot.ally_behaviour import AllyBehaviour
from chuckle_bot.ally_vocabulary import AllyVocabulary
from chuckle_bot.characters import Characters, ICharacter


ALLIES_INDEXER = lambda c: c.name.lower()


def build_allies(raw_allies):
    allies = Characters([], ALLIES_INDEXER)
    for raw_ally in raw_allies:
        ally = Ally(raw_ally)
        ally.set_behaviour(AllyBehaviour(ally))
        ally.set_vocabulary(AllyVocabulary(ally))
        allies.add(ally)
    return allies


class Ally(ICharacter):
    def __init__(self, data):
        self._data = data
        self._behaviour = None
        self._vocabulary = None

    def set_behaviour(self, behaviour):
        self._behaviour = behaviour

    def set_vocabulary(self, vocabulary):
        self._vocabulary = vocabulary

    @property
    def name(self):
        return self._data["CHAR_NICK"]

    @property
    def full_name(self):
        return self._data["CHAR_FULL"]

    @property
    def class_(self):
        return self._data["CLASS"]

    @property
    def race(self):
        raise self._data["RACE"]

    def send_message(self, msg):
        return self._behaviour.send_message(msg)

    def get_action(self):
        chosen_action = self._behaviour.get_action()
        return self._vocabulary.announce_action(chosen_action)
