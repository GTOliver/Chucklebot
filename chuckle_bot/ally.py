from chuckle_bot.icharacter import ICharacter


class Allies:
    def __init__(self, ally_list):
        self._ally_list = ally_list

    def get(self, name):
        for ally in self._ally_list:
            if name.lower() == ally["CHAR_NICK"].lower():
                return Ally(ally)


class Ally(ICharacter):
    def __init__(self, data):
        self._data = data

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
