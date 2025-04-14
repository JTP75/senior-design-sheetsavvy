from xml.etree.ElementTree import Element, ElementTree, SubElement


class Note(Element):
    parent: any
    pitch: dict
    note_type: str
    duration: int
    dot: bool
    beam: str
    tied: str

    def __init__(self,
                 parent: any,
                 default_x: int,
                 pitch: dict,
                 note_type: str,
                 duration: int,
                 dot: bool=False,
                 tied: str=""):
        self.parent = parent
        self.pitch = pitch
        self.note_type = note_type
        self.duration = duration
        self.dot = dot
        self.beam = ""
        self.tied = tied
        super().__init__("note",{"default-x":str(default_x)})
        self._put_attrib()

    def is_rest(self) -> bool:
        return not self.pitch

    def _put_attrib(self):
        if self.pitch:
            t_pitch = SubElement(self,"pitch")
            for tag in self.pitch:
                t = SubElement(t_pitch,tag)
                t.text = str(self.pitch[tag])
        else:
            SubElement(self,"rest")
        t_duration = SubElement(self,"duration")
        t_duration.text = str(self.duration)
        t_type = SubElement(self,"type")
        t_type.text = self.note_type
        if self.dot:
            SubElement(self,"dot")
        if self.tied=="continue":
            SubElement(self,"tie",{"type": "start"})
            t_notations = SubElement(self, "notations")
            SubElement(t_notations,"tied",{"type": "start"})
            SubElement(t_notations,"tied",{"type": "stop"})
        elif self.tied!="":
            SubElement(self,"tie",{"type":self.tied})
            t_notations = SubElement(self, "notations")
            SubElement(t_notations,"tied",{"type": self.tied})

    def set_beam(self, beam: str):
        self.beam = beam
        t_beam = SubElement(self,"beam")
        t_beam.text = self.beam