from xml.etree.ElementTree import ElementTree

from src.framework.measure import Measure


class Score(ElementTree):

    measures: list

    def __init__(self, base_path):
        super().__init__(file=base_path)
        self.measures = []

    def insert_measure(self, index: int, measure: "Measure"):
        self.find("part").insert(index, measure)
        self.measures.insert(index, measure)

    def append_measure(self, measure: "Measure"):
        self.insert_measure(len(self.measures),measure)
        self.measures.append(measure)