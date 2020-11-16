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

