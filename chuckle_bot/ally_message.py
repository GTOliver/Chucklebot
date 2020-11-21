"""
AllyMessages are things which are said to allies

AllyMessages are said to either all, or certain specific people.
This is represented by the "target".

Types of message:

*   <CHAR> SHOULD ATTACK
*   <CHAR> SHOULD RETREAT
*   <CHAR> SHOULD WAIT
*   <CHAR_A> SHOULD SUPPORT <CHAR_B>
*   <ALL> SHOULD SUPPORT <CHAR_B>
*   PRAISE <CHAR>
*   REBUKE <CHAR>
"""


class AllyMessage:
    def __init__(self, sender, type_, subject, secondary_subject=None):
        self.sender = sender
        self.type_ = type_
        self.subject = subject
        self.secondary_subject = secondary_subject

    def __eq__(self, other):
        sender_is_same = self.sender == other.sender
        type_is_same = self.type_ == other.type_
        subject_is_same = self.subject == other.subject
        secondary_is_same = self.secondary_subject == other.secondary_subject
        return sender_is_same and type_is_same and subject_is_same and secondary_is_same

    def __repr__(self):
        return ' '.join([self.sender, self.type_, self.subject, self.secondary_subject])


def attack(sender, who_should_attack):
    return AllyMessage(sender, "ATTACK", who_should_attack)


def retreat(sender, who_should_retreat):
    return AllyMessage(sender, "RETREAT", who_should_retreat)


def wait(sender, who_should_wait):
    return AllyMessage(sender, "WAIT", who_should_wait)


def support(sender, who_should_support, who_needs_support):
    return AllyMessage(sender, "SUPPORT", who_should_support, who_needs_support)


def praise(sender, target):
    return AllyMessage(sender, "PRAISE", target)


def rebuke(sender, target):
    return AllyMessage(sender, "REBUKE", target)