
from typing import Any


class Entity():
    __attributes__ = ['matches', 'label', 'tag']
    
    def __init__(
            self, matches:object, label:str, tag:str):
        self.matches = matches
        self.label = label
        self.tag = tag 


def isempty(parser, text) -> bool:
    return not parser.find(text)
    

class Extractor():
    def __init__(self, rules:list):
        self.parsers = []     
        from yargy import Parser
        for _ in rules:
            self.parsers.append(Parser(_.rule))
        self.rules = rules

    def empty(self, text) -> bool:
        for p in self.parsers:
            empty = isempty(parser=p, text=text) 
            if not empty:
                return False 
        return True

    def __call__(self, text) -> list:
        entities = []
        for p, r in zip(self.parsers, self.rules):
            if not isempty(parser=p, text=text):
               matches = p.findall(text)
               entities.append(
                   Entity(matches, r.label, r.tag)) 
        return entities
    

    




