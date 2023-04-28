
from .rules.label import(
    CONTRACT,
    GUARANTEE
)
from .rules.add_rules import(
    ADDITIONAL
)
from .rules.amount import(
    MONEY,
    PERCENT,
    AMOUNT
)

from yargy import Parser

from ipymarkup import show_span_box_markup



class Mark():
    __attributes__ = ['start', 'stop', 'type']

    def __init__(self, start, stop, type):
        if start >= stop:
            raise ValueError('invert mark: (%r, %r)' % (start, stop))
        self.start = start
        self.stop = stop
        self.type = type
    
    def __repr__(self):
        return '(%d, %d, %s)' % (self.start, self.stop, self.type)
    
    def to_tuple(self):
        return (self.start, self.stop, self.type)
      


def get_label(label):
    label1 = "обеспечение исполнения контракта"
    label2 = "обеспечение гарантийных обязательств"
    return label1 if label == label1 else label2


def switch_labels(label):
    if label == get_label(label):
        return '1'
    if label == get_label(label):
        return '2'
    raise Exception("No label found!") 


def drop_label(label):
    return '2' if label == '1' else '1'

def switch_parser(type):
    if type == '1':
        return CONTRACT
    if type == '2':
        return GUARANTEE
    if type == '+':
        return ADDITIONAL
    if type == '$':
        return MONEY
    if type == '%':
        return PERCENT
    raise Exception("No case found!")


def get_matches(text, type):
    RULE = switch_parser(type=type)
    parser = Parser(RULE)
    return parser.findall(text) 


def prepare_marks(marks, type):
    pre_marks = []
    for mark in marks:
        pre_marks.append(Mark(mark.start, mark.stop, type))
    return pre_marks


def get_marks(text, type):
    matches = get_matches(
        text, 
        type
    )
    marks = [_.span for _ in matches]
    
    return prepare_marks(marks, type)


def get_parsers(label):
    parsers = ['1', '2', '+', '$', '%']
    label = switch_labels(label) 
    parsers.remove(drop_label(label))
    return parsers


def show_markup(text, marks):
    show_span_box_markup(text, (
            _.to_tuple() for _ in marks
            )
        )
