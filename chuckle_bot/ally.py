from chuckle_bot.ally_behaviour import AllyBehaviour
from chuckle_bot.icharacter import ICharacter


def build_allies(raw_allies):
    ally_dict = {}
    for raw_ally in raw_allies:
        ally = Ally(raw_ally)
        ally.set_behaviour(AllyBehaviour(ally))
        ally_dict[ally.name.lower()] = ally
    return Allies(ally_dict)


class Allies:
    def __init__(self, ally_dict):
        self._ally_dict = ally_dict

    def get(self, name):
        try:
            return self._ally_dict[name.lower()]
        except KeyError:
            return None

    def add(self, name, ally):
        self._ally_dict[name.lower()] = ally


class Ally(ICharacter):
    def __init__(self, data):
        self._data = data
        self._behaviour = None

    def set_behaviour(self, behaviour):
        self._behaviour = behaviour

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

    def take_turn(self):
        return self._behaviour.take_turn()
