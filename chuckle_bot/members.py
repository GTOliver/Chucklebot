class Members:
    def __init__(self, member_list):
        self._member_list = member_list

    def get(self, member_id):
        for member in self._member_list:
            if member["ID"] == member_id:
                return member
        return None
