class Encounter:
    def __init__(self, player_characters):
        self._characters = player_characters
        self._allies = []
        self._active = False

    def add_ally(self, ally):
        self._allies.append(ally)

    def begin(self):
        self._active = True
        return "The encounter begins!"

    def end(self):
        self._active = False
        return "The encounter ends!"

    def reset(self):
        self._allies = []
        self._active = False
        return "Ready to start a new encounter..."

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
