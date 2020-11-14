class ChuckleCount:
    def __init__(self, chuckle_data):
        self._chuckle_data = chuckle_data

    def get_count(self, character_id):
        for elem in self._chuckle_data:
            if elem["CHAR_ID"] == character_id:
                return elem["COUNT"]
        return 0

    def get_all(self):
        return self._chuckle_data
