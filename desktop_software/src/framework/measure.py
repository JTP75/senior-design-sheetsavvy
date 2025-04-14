from email.policy import default
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from src.framework.app_constants import DEFAULT_DIVISIONS
from src.framework.note import Note


class Measure(Element):

    number: int
    parent: any
    notes: list
    begin: int
    end: int

    def __init__(self, parent: any, number: int, width: int, begin: int, end: int):
        self.parent = parent
        self.number = number
        self.begin = begin
        self.end = end
        self.notes = []
        super().__init__("measure",{"number":str(self.number), "width":str(width)})

    def add_note(self, default_x: int, note_dict: dict):
        new_note = Note(
            self,
            default_x,
            note_dict["pitch"],
            note_dict["type"],
            note_dict["duration"],
            note_dict["dot"] if "dot" in note_dict.keys() else False,
            note_dict["tie"] if "tie" in note_dict.keys() else ""
        )
        self.notes.append(new_note)
        self.append(new_note)

    def add_beam(self, from_index: int, to_index: int):
        self.notes[from_index].set_beam("begin")
        for index in range(from_index+1,to_index):
            self.notes[index].set_beam("continue")
        self.notes[to_index].set_beam("end")

    @property
    def duration(self):
        return self.end - self.begin

    def add_attribute(self, ):
        pass

    def add_direction(self, ):
        pass