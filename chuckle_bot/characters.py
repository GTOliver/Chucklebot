class ICharacter:
    @property
    def name(self):
        raise NotImplementedError

    @property
    def full_name(self):
        raise NotImplementedError

    @property
    def class_(self):
        raise NotImplementedError

    @property
    def race(self):
        raise NotImplementedError


class Characters:
    def __init__(self, character_list, indexer):
        self._character_list = character_list
        self._indexer = indexer

    def get(self, key):
        for character in self._character_list:
            if self._indexer(character) == key:
                return character

    def get_subset(self, keys):
        return Characters([self.get(key) for key in keys], self._indexer)

    def add(self, new_character):
        self._character_list.append(new_character)

    def __iter__(self):
        return self._character_list.__iter__()

    def __len__(self):
        return self._character_list.__len__()

