from chuckle_bot.characters import ICharacter, Characters


PLAYERS_INDEXER = lambda c: c.id


def build_players(raw_characters):
    player_list = [Player(rc) for rc in raw_characters]
    return Characters(player_list, PLAYERS_INDEXER)


class Player(ICharacter):
    def __init__(self, character_data):
        self._data = character_data

    @property
    def name(self):
        return self._data['CHAR_NICK']

    @property
    def full_name(self):
        return self._data['CHAR_FULL']

    @property
    def class_(self):
        return self._data['CLASS']

    @property
    def race(self):
        return self._data['RACE']

    @property
    def pronouns(self):
        return self._data["PRONOUNS"]

    @property
    def id(self):
        return self._data['CHAR_ID']

    def get_modifier(self, stat_or_skill):
        if stat_or_skill not in self._data['STATS']:
            # It needs a proficiency modifier
            skill = stat_or_skill
            for stat_proficiencies in self._data['PROFICIENCY']:
                if skill in self._data['PROFICIENCY'][stat_proficiencies]:
                    proficiency_multiplier = self._data['PROFICIENCY'][stat_proficiencies][skill]
                    relevant_stat = stat_proficiencies
                    break
        else:
            proficiency_multiplier = 0
            relevant_stat = stat_or_skill

        stat_value = self._data['STATS'][relevant_stat]
        stat_modifier = int((stat_value - 10)/2)
        result = stat_modifier + self._data['PROFICIENCY_BONUS'] * proficiency_multiplier
        return result

    def all_options(self):
        options = []
        for stat_dict in self._data['PROFICIENCY']:
            options.append(stat_dict)
            for key in self._data['PROFICIENCY'][stat_dict]:
                options.append(key)
        return options
