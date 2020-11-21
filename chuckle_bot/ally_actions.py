class AllyAction:
    def __init__(self, action, target=None):
        self.type_ = action
        self.target = target


def attack():
    """
    An ATTACK command means attacking a nearby creature
    """
    return AllyAction("ATTACK")


def retreat():
    """
    A RETREAT action means getting back to safety
    """
    return AllyAction("RETREAT")


def wait():
    """
    A WAIT action means doing nothing
    """
    return AllyAction("WAIT")


def support(target):
    """
    A SUPPORT action means supporting a particular party member
    """
    return AllyAction("SUPPORT", target)
