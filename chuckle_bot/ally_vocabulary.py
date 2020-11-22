import random


def random_entry(input_list):
    return input_list[random.randint(0, len(input_list) - 1)]


class AllyVocabulary:
    def __init__(self, ally):
        self._ally = ally

    def begin_encounter(self):
        return self._ally.name + " is present at the beginning of the encounter."

    def end_encounter(self):
        return self._ally.name + " is present at the end of the encounter."

    def send_message(self, msg):
        return self._ally.name + " received the message."

    def announce_action(self, action):
        """ Get a text version of the action """
        response = self._ally.name + " will " + action.type_.lower()
        if action.target is not None:
            response += " " + action.target.name
        return response

    def reset(self):
        pass


class RandomisedVocabulary(AllyVocabulary):
    def begin_encounter(self):
        return self._ally.name + " says \"" + random_entry(self._BEGIN) + "\""

    def end_encounter(self):
        return self._ally.name + " says \"" + random_entry(self._END) + "\""

    def send_message(self, msg):
        if msg.type_ in ["REBUKE", "PRAISE"]:
            response = self._ally.name + " says: \""
            response += random_entry(getattr(self, "_" + msg.type_))
            response += "\""
            response = response.replace('_x', self._ally.name)
            response = response.replace('_s', msg.sender.name)
            return response

    def announce_action(self, action):
        pre = getattr(self, "_" + action.type_ + "_PRE")
        mid = getattr(self, "_" + action.type_ + "_MID")
        pst = getattr(self, "_" + action.type_ + "_PST")

        r_pre = random_entry(pre)
        r_mid = "\"" + random_entry(mid) + "\""
        r_pst = random_entry(pst)
        msg = ' '.join([r_pre, r_mid, r_pst]).strip()
        msg = msg.replace('_x', self._ally.name)
        msg = msg.replace('_pr', self._ally.pronouns["PERSONAL"])
        msg = msg.replace('_ps', self._ally.pronouns["POSSESSIVE"])
        msg = msg.replace('_po', self._ally.pronouns["OBJECTIVE"])
        if action.target is not None:
            msg = msg.replace('_tn', action.target.name)
            msg = msg.replace('_tpr', action.target.pronouns["PERSONAL"])
            msg = msg.replace('_tps', action.target.pronouns["POSSESSIVE"])
            msg = msg.replace('_tpo', action.target.pronouns["OBJECTIVE"])
        return msg

    _BEGIN = [""]
    _END = [""]
    _REBUKE = [""]
    _PRAISE = [""]
    _ATTACK_PRE = [""]
    _ATTACK_MID = [""]
    _ATTACK_PST = [""]
    _WAIT_PRE = [""]
    _WAIT_MID = [""]
    _WAIT_PST = [""]
    _RETREAT_PRE = [""]
    _RETREAT_MID = [""]
    _RETREAT_PST = [""]
    _SUPPORT_PRE = [""]
    _SUPPORT_MID = [""]
    _SUPPORT_PST = [""]


class AcademicVocabulary(RandomisedVocabulary):
    """ An academic vocabulary is inquisitive, knowledgeable and perceptive """
    _ATTACK_PRE = [
        "_x says"
    ]
    _ATTACK_MID = [
        "I think the best thing to do in this situation is ... attack!",
        "This situation calls for an attack!",
        "By my calculations, I should attack.",
        "It's time for an attack!",
        "I am sure the best thing for right now is an attack!",
    ]
    _ATTACK_PST = [
        ""
    ]
    _WAIT_PRE = [
        "_x eyes the situation inquisitively and says",
        "_x gawks open-mouthed at the situation and tries to take it all it. _pr says",
        "_x says",
        "_x looks at the situation in wonder, and says",
    ]
    _WAIT_MID = [
        "... I wish I was recording this",
        "Wow! This is amazing!",
        "I've not observed a specimen like this before!",
        "Absolutely marvelous",
        "What an interesting development",
        "How interesting",
        "Perfectly splendid"
        ""
    ]
    _WAIT_PST = [
        "and _pr doesn't do anything of use.",
        "and _pr waits for something else to happen.",
        "and _pr continues to watch."
    ]
    _RETREAT_PRE = [
        "_x looks scared, and tries to run to safety. _pr says",
        "_x retreats to safety and shouts",
        "_x runs away screaming",
        "_x turns and runs while yelling"
    ]
    _RETREAT_MID = [
        "Oh no!!",
        "Ahh!!",
        "Gotta get out of here!",
        "I... shouldn't be here...",
        "I've got to get away",
        "This isn't where I'm supposed to be...",
        "I shouldn't be here...",
        "I wish I was just reading about this in a book, not living it!"
    ]
    _RETREAT_PST = [
        "",
        "and flails around wildly.",
        "and sweats excessively.",
        "and lets out a nervous toot."
    ]
    _SUPPORT_PRE = [
        "_x says",
    ]
    _SUPPORT_MID = [
        "I'm coming, _tn!",
        "You need my help _tn, let me assist!"
    ]
    _SUPPORT_PST = [
        "and runs over to help _tpo.",
        "and gives _tpo a hand.",
        "and helps _tpo.",
    ]
    _REBUKE = [
        "Hey... that's not fair...",
        "I.. I.. I'm sorry _s.",
        "I.. didn't anticipate it, _s.",
        "My calculations were wrong...",
        "I am sad now.",
        "My heart is heavy."
    ]
    _PRAISE = [
        "I have a very high IQ.",
        "Thanks, _s.",
        "I am rather remarkable.",
        "My intelligence is unmatched.",
        "My last move was a 500 IQ play.",
    ]
    _BEGIN = [
        "Oh no...",
    ]
    _END = [
        "I'm glad that's over!",
        "Phew!",
    ]


ALLY_VOCABULARY = {
    "terse": AllyVocabulary,
    "academic": AcademicVocabulary,
}
