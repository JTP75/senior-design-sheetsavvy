class SheetMusicGenerator:

    def generate(self):
        """Populate sheet music XML tree

        **Pre**: ``set_note_data()`` has been called

        **Post**: Sheet music tree is filled and ready to be saved

        **throws**: ``SheetMusicGeneratorException``"""
        pass
    def save_as(self, location: str):
        pass
    def add_first_measure(self):
        pass
    def add_measure(self, begin: int, end: int):
        pass
    def set_note_data(self, data):
        pass
    def set_attr_data(self, data):
        pass