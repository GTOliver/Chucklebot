from chuckle_bot.ally_message import AllyMessage
from chuckle_bot.interpreter import Interpreter


def dummy_encounter_context():
    class DummyEncounterContext:
        def __init__(self):
            self.participants = ['char_a', 'char_b']
    return DummyEncounterContext()


def dummy_interpreter():
    return Interpreter(dummy_encounter_context())


def test_init():
    assert dummy_interpreter() is not None


def test_words_no_punctuation():
    msg = "foo bar baz bazaar"
    expected = ["foo", "bar", "baz", "bazaar"]
    returned = Interpreter._get_lwords(msg)
    assert expected == returned


def test_words_no_punctuation2():
    msg = "Foo bAR baz bazaar"
    expected = ["foo", "bar", "baz", "bazaar"]
    returned = Interpreter._get_lwords(msg)
    assert expected == returned


def test_words_punctuation():
    msg = "Foo bAR!! baz- bazaar."
    expected = ["foo", "bar", "baz", "bazaar"]
    returned = Interpreter._get_lwords(msg)
    assert expected == returned


def test_nonsense_a():
    sender = "char_0"
    msg = "adsfasdf"
    result = dummy_interpreter().interpret(sender, msg)
    assert result is None


def test_attack():
    sender = "char_0"
    msg = "char_a attack"
    result = dummy_interpreter().interpret(sender, msg)
    expected_msg = AllyMessage(
        "char_0", "ATTACK", "char_a", None
    )
    assert result == expected_msg


def test_create_placeholder():
    words = ['hello', 'foo', 'bar', 'bazaar', 'foo']
    replaceables = ['foo', 'bazaar', 'xxx']

    def placeholder_factory(idx):
        return "__" + str(idx) + "__"

    ret_words, ret_alii = Interpreter._create_placeholders(words, replaceables, placeholder_factory)
    exp_words, exp_alii = ['hello', '__0__', 'bar', '__1__', '__0__'], ['foo', 'bazaar']

    assert ret_words == exp_words
    assert ret_alii == exp_alii


def test_simple_words():
    words = ['attack', '__0']
    expected_expr = ['attack', '__0']
    returned_expr = Interpreter._simplify(words)
    assert expected_expr == returned_expr