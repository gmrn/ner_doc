
class Entity():
    __attributes__ = ['matches', 'label', 'tag']
    
    def __init__(self, label, tag):
        self.matches = []
        self.label = label
        self.tag = tag



def find_matches(parser, text):
    return parser.findall(text)
    

class Extractor():
    
    def __init__(self, rules):
        from yargy import Parser
        self.parsers = []
        self.entities = []
        for _ in rules:
            try:
                self.parsers.append(
                    Parser(_.rule))
                self.entities.append(
                    Entity(_.label, _.tag))
            except: 
                raise ValueError('rule must to include RULE, label, tag')      

    def __call__(self, text):
        for _, __ in zip(self.parsers, 
                             self.entities):
            __.matches = find_matches(_, text)

        return self.entities
    




