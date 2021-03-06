from chuckle_bot.ally import ALLIES_INDEXER
from chuckle_bot.characters import Characters


class Encounter:
    def __init__(self, player_characters):
        self._characters = player_characters
        self._allies = Characters([], ALLIES_INDEXER)
        self._active = False

    def get_action(self, char_name):
        return self._allies[char_name].get_action()

    def say(self, message):
        if message.subject == "ALL":
            responses = []
            for ally in self._allies:
                if (response := ally.send_message(message)) is not None:
                    responses.append(response)
            return '\n'.join(responses)
        return message.subject.send_message(message)

    def add_ally(self, ally):
        self._allies.add(ally)

    def begin(self):
        self._reset_allies()
        self._active = True
        ally_responses = [a.begin_encounter() for a in self._allies]
        title = "The encounter begins!"
        return title + "\n" + "\n".join(ally_responses)

    def end(self):
        self._reset_allies()
        self._active = False
        ally_responses = [a.end_encounter() for a in self._allies]
        title = "The encounter ends!"
        return title + "\n" + "\n".join(ally_responses)

    def reset(self):
        self._remove_allies()
        self._active = False
        return "Ready to start a new encounter..."

    @property
    def participants(self):
        ichars = list(self._allies)
        ichars.extend(list(self._characters))
        names = [ic.name for ic in ichars]
        return names

    def get_participant(self, char_name):
        found = self._allies[char_name]
        if found is not None:
            return found
        for pc in self._characters:
            if pc.name.lower() == char_name.lower():
                return pc

    def __repr__(self):
        lines = []
        if self._active:
            lines.extend(
                ["In an encounter!",
                 "Active players:"])
        else:
            lines.extend(
                ["Not in an encounter at the moment!",
                 "Players ready:"]
            )

        indent = "    "
        lines.extend([indent + x.full_name for x in self._characters])

        if len(self._allies) != 0:
            if self._active:
                lines.append("Active allies:")
            else:
                lines.append("Allies ready:")
            lines.extend([indent + x.full_name for x in self._allies])
        return '\n'.join(lines)

    def _reset_allies(self):
        for ally in self._allies:
            ally.reset()

    def _remove_allies(self):
        self._reset_allies()
        self._allies = Characters([], ALLIES_INDEXER)
