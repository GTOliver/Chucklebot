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
        return self._get_msg("BEGIN")

    def end_encounter(self):
        return self._get_msg("END")

    def send_message(self, msg):
        if msg.type_ in ["REBUKE", "PRAISE"]:
            return self._get_msg(msg.type_, msg.sender)

    def announce_action(self, action):
        return self._get_msg(action.type_, action.target)

    def _get_msg(self, type_, target=None):
        msg = random_entry(getattr(self, "_" + type_))
        return self._replace_names_and_pronouns(msg, target)

    def _replace_names_and_pronouns(self, msg, target=None):
        msg = msg.replace('_x', self._ally.name)
        msg = msg.replace('_pr', self._ally.pronouns["PERSONAL"])
        msg = msg.replace('_ps', self._ally.pronouns["POSSESSIVE"])
        msg = msg.replace('_po', self._ally.pronouns["OBJECTIVE"])
        if target is not None:
            msg = msg.replace('_tn', target.name)
            msg = msg.replace('_tpr', target.pronouns["PERSONAL"])
            msg = msg.replace('_tps', target.pronouns["POSSESSIVE"])
            msg = msg.replace('_tpo', target.pronouns["OBJECTIVE"])
        return msg

    _BEGIN = [""]
    _END = [""]
    _REBUKE = [""]
    _PRAISE = [""]
    _ATTACK = [""]
    _WAIT = [""]
    _RETREAT = [""]
    _SUPPORT = [""]


class AcademicVocabulary(RandomisedVocabulary):
    """ An academic vocabulary is inquisitive, knowledgeable and perceptive """
    _ATTACK = [
        "_x says \"The best thing to do in this situation is ... attack!\"",
        "_x says \"This situation calls for an attack!\"",
        "_x says \"It's time for an attack!\"",
        "_x hefts their weapon and attacks the enemy.",
    ]
    _WAIT = [
        "_x doesn't do anything of use.",
        "_x waits for something else to happen.",
        "_x says \"Perfectly splendid\" and continues to watch.",
        "_x says \"How interesting!\" and makes some notes in _pr notebook.",
        "_x considers the situation and takes their bearings.",
    ]
    _RETREAT = [
        "_x looks scared and tries to run to safety.",
        "_x considers that discretion is the better part of valour and retreats from danger.",
        "_x runs away screaming \"Aaaah!\"",
        "_x says \"Oh no!!\" and flails around wildly.",
    ]
    _SUPPORT = [
        "_x says \"I'm coming, _tn\"!",
        "_x rushes to _tn's aid.",
        "_x runs to help _tn.",
        "_x concludes that _tn is in peril, and rushes to help _top."
    ]
    _REBUKE = [
        "_x says \"Hey... that's not fair...\"",
        "_x says \"I.. I.. I'm sorry _tn.\"",
        "_x says \"I.. didn't anticipate it, _tn.\"",
        "_x says \"I am sad now.\"",
        "_x rolls _ps eyes.",
    ]
    _PRAISE = [
        "_x says \"I have a very high IQ.\"",
        "_x says \"Thanks, _tn.\"",
        "_x says \"I am rather remarkable.\"",
        "_x says \"My intelligence is unmatched.\"",
        "_x says \"My last move was a 500 IQ play.\"",
        "_x nods _ps head appreciatively."
    ]
    _BEGIN = [
        "_x says \"Oh no...\"",
    ]
    _END = [
        "_x says \"I'm glad that's over!\"",
        "_x breathes a sigh of relief.",
    ]


class ConfidentVocabulary(RandomisedVocabulary):
    """ A confident vocabulary is ... confident and adept """
    _ATTACK = [
        "_x says \"Hah! Time for an attack!!\"",
        "_x says \"I will attack!!\"",
        "_x says \"Aaaattttacckkk!!\"",
        "_x attacks!!.",
    ]
    _WAIT = [
        "_x ponders...",
        "_x waits attentively...",
        "_x pauses for a moment...",
        "_x waits a moment...",
    ]
    _RETREAT = [
        "_x moves to safer ground.",
        "_x retreats from danger and steadies themselves.",
        "_x moves to a safer area...",
    ]
    _SUPPORT = [
        "_x says \"I'm coming, _tn\"!",
        "_x rushes to _tn's aid.",
        "_x runs to help _tn.",
    ]
    _REBUKE = [
        "_x says \"Hey...\"",
        "_x says \"Pah!\"",
        "_x says \"Nonsense, _tn.\"",
        "_x says \"That's not true!\"",
        "_x rolls _ps eyes.",
    ]
    _PRAISE = [
        "_x says \"Hah hah, quite right!.\"",
        "_x says \"Indeed, _tn.\"",
        "_x says \"Yes!\"",
        "_x says \"Oh ho ho!.\"",
    ]
    _BEGIN = [
        "_x says \"Aha! A fight...!\"",
    ]
    _END = [
        "_x says \"Well well...\"",
        "_x says \"Good job crew!\"",
        "_x says \"We sure showed them!\"",
    ]


class NonverbalVocabulary(RandomisedVocabulary):
    """ A nonverbal vocabulary ... can't speak """
    _ATTACK = [
        "_x makes a guttural noise and attacks!",
        "_x attacks with a grunt",
        "_x attacks!",
        "_x grunts and attacks!",
    ]
    _WAIT = [
        "_x looks around...",
        "_x waits attentively...",
        "_x grunts.",
    ]
    _RETREAT = [
        "_x rushes away to safer ground.",
        "_x retreats from danger...",
        "_x moves to a safer place.",
        "_x grunts and retreats.",
    ]
    _SUPPORT = [
        "_x rushes to _tn's aid.",
        "_x runs to help _tn.",
        "_x grunts... (and helps _tn)",
    ]
    _REBUKE = [
        "_x grunts angrily",
        "_x makes some angry noises in the direction of _tn",
        "_x grunts.",
    ]
    _PRAISE = [
        "_x grunts appreciatively",
        "_x nods",
        "_x grunts.",
    ]
    _BEGIN = [
        "_x grunts.",
    ]
    _END = [
        "_x grunts.",
    ]


ALLY_VOCABULARY = {
    "terse": AllyVocabulary,
    "academic": AcademicVocabulary,
    "confident": ConfidentVocabulary,
    "nonverbal": NonverbalVocabulary,
}
