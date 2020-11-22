class Members:
    def __init__(self, member_list):
        self._member_list = member_list

    def __getitem__(self, member_id):
        for member in self._member_list:
            if member["ID"] == member_id:
                return member

    def char_id(self, member_id):
        return self[member_id]["CHAR_ID"]
