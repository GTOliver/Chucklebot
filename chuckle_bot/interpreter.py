""" Interpret human-sent messages as AllyMessages """

from chuckle_bot import ally_message as am


class Interpreter:
    _SENDER_PLACEHOLDER = "_x"

    def __init__(self, encounter_context):
        # The interpreter keeps the encounter context so that it
        # is able to get the names of all the participants
        self._encounter_context = encounter_context

    @staticmethod
    def _placeholder_string(idx):
        return "_" + str(idx)

    @classmethod
    def _get_lwords(cls, message):
        """ Get all words in lower-case """
        punctuation_marks = ".,!?-:()'_"
        for mark in punctuation_marks:
            message = message.replace(mark, '')
        return message.lower().split(' ')

    @classmethod
    def _create_placeholders(cls, words, replaceable, placeholder_factory):
        placeholder_alii = []
        legit_words = []
        for word in words:
            if word in placeholder_alii:
                placeholder_idx = placeholder_alii.index(word)
                placeholder_used = placeholder_factory(placeholder_idx)
                legit_words.append(placeholder_used)
            elif word in replaceable:
                placeholder = placeholder_factory(len(placeholder_alii))
                placeholder_alii.append(word)
                legit_words.append(placeholder)
            else:
                legit_words.append(word)
        return legit_words, placeholder_alii

    @staticmethod
    def _replace_sender(words, sender_placeholder):
        new_words = []
        triggers = ["i", "me", "my", "we", "us", "our"]
        for word in words:
            if word in triggers:
                new_words.append(sender_placeholder)
            else:
                new_words.append(word)
        return new_words

    @staticmethod
    def _simplify(words):
        simple_words = []
        for word in words:
            if word.startswith('_'):
                simple_words.append(word)
            else:
                for key, vals in SIMPLIFY_THESAURUS.items():
                    if word == key or word in vals:
                        simple_words.append(key)
                        break
        return simple_words

    def interpret(self, sender, message):
        participants = self._encounter_context.participants
        lparticipants = [p.lower() for p in participants]

        words = self._get_lwords(message)
        words = self._replace_sender(words, self._SENDER_PLACEHOLDER)

        words, alii = self._create_placeholders(words, lparticipants,
                                                Interpreter._placeholder_string)
        simple_words = self._simplify(words)

        matched_pattern = self._matched_pattern(
            sender.lower(), self._SENDER_PLACEHOLDER, alii, simple_words)

        if matched_pattern is None:
            return
        func = matched_pattern[0]
        args = [sender]
        for targ in matched_pattern[1:]:
            if targ == self._SENDER_PLACEHOLDER:
                args.append(sender)
            elif targ.startswith('_'):
                args.append(alii[int(targ[1:])])

        actual_args = []
        for arg in args:
            if arg == "ALL":
                actual_args.append(arg)
            else:
                actual_args.append(self._encounter_context.get_participant(arg))
        return func(*actual_args)

    @staticmethod
    def _matched_pattern(sender, sender_placeholder, alii, simple_words):
        """
        pattern = []
        for word in simple_words:
            if word.startswith("_"):
                pattern.append("_")
            else:
                pattern.append(word)
        """
        for pattern, instruction in KNOWN_PATTERNS:
            if simple_words == pattern:
                return instruction


SIMPLIFY_THESAURUS = {
    'attack': [
        'slay', 'hit', 'kill', 'target', 'strike',
    ],
    'retreat': [
        'flee', 'run', 'safety', 'careful', 'away',
    ],
    'wait': [
        'hold', 'pause',
    ],
    'support': [
        'help', 'assist', 'heal',
    ],
    'praise': [
        'good', 'great', 'nice', 'awesome', 'sick',
    ],
    'rebuke': [
        'bad', 'damn', 'damnit', 'poor',
    ],
    'inverse': [
        'dont', 'not',
    ],
}


KNOWN_PATTERNS = [
    (["_0", "attack"], (am.attack, "_0")),
    (["attack", "_0"], (am.attack, "_0")),
    (["_x", "_0", "attack"], (am.attack, "_0")),
    (["_0", "attack", "rebuke"], (am.attack, "_0")),
    (["attack", "rebuke", "_0"], (am.attack, "_0")),
    (["_x", "_0", "attack", "rebuke"], (am.attack, "_0")),
    (["_0", "inverse", "attack"], (am.wait, "_0")),
    (["inverse", "attack", "_0"], (am.wait, "_0")),

    (["_0", "retreat"], (am.retreat, "_0")),
    (["_0", "retreat", "retreat"], (am.retreat, "_0")),
    (["retreat", "_0"], (am.retreat, "_0")),
    (["retreat", "retreat", "_0"], (am.retreat, "_0")),
    (["_x", "_0", "retreat"], (am.retreat, "_0")),
    (["_x", "_0", "retreat", "retreat"], (am.retreat, "_0")),
    (["_x", "retreat", "_0"], (am.retreat, "_0")),
    (["_x", "retreat", "retreat", "_0"], (am.retreat, "_0")),
    (["_0", "inverse", "retreat"], (am.attack, "_0")),
    (["_0", "inverse", "retreat", "retreat"], (am.attack, "_0")),
    (["inverse", "retreat", "_0"], (am.attack, "_0")),
    (["inverse", "retreat", "retreat", "_0"], (am.attack, "_0")),
    (["_x", "_0", "inverse", "retreat"], (am.attack, "_0")),
    (["_x", "_0", "inverse", "retreat", "retreat"], (am.attack, "_0")),
    (["_x", "inverse", "retreat", "_0"], (am.attack, "_0")),
    (["_x", "inverse", "retreat", "retreat", "_0"], (am.attack, "_0")),

    (["_0", "wait"], (am.wait, "_0")),
    (["wait", "_0"], (am.wait, "_0)")),

    (["_x", "support"], (am.support, "ALL", "_x")),
    (["support", "_x"], (am.support, "ALL", "_x")),
    (["_0", "support"], (am.support, "ALL", "_0")),
    (["support", "_0"], (am.support, "ALL", "_0")),
    (["support", "_x", "_0"], (am.support, "_0", "_x")),
    (["_0", "support", "_x"], (am.support, "_0", "_x")),
    (["_0", "_x", "support"], (am.support, "_0", "_x")),
    (["_0", "support", "_x"], (am.support, "_0", "_x")),
    (["_x", "support", "_0"], (am.support, "_x", "_0")),
    (["_x", "support", "_0"], (am.support, "_x", "_0")),
    (["support", "_0", "_1"], (am.support, "_1", "_0")),
    (["_0", "support", "_1"], (am.support, "_0", "_1")),    # _0, help _1
    # If someone says "_0 needs help, _1" it will be interpreted incorrectly.

    (["praise", "_0"], (am.praise, "_0")),
    (["_0", "praise"], (am.praise, "_0")),
    (["inverse", "praise", "_0"], (am.rebuke, "_0")),
    (["_0", "inverse", "praise"], (am.rebuke, "_0")),
    (["rebuke", "_0"], (am.rebuke, "_0")),
    (["_0", "rebuke"], (am.rebuke, "_0")),
    (["inverse", "rebuke", "_0"], (am.praise, "_0")),
    (["_0", "inverse", "rebuke"], (am.praise, "_0")),
]
