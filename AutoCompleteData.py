# coding: utf-8
from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


    def __str__(self):
        return f"c'{self.completed_sentence}', ('{self.source_text}'{self.offset}) , score={self.score}"
        #return f"completed_sentence='{self.completed_sentence}', source_text='{self.source_text}', offset={self.offset}, score={self.score}"
