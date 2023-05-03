
class Mark():
    __attributes__ = ['start', 'stop', 'tag']

    def __init__(self, start, stop, tag = None):
        if start >= stop:
            raise ValueError('invert mark: (%r, %r)' % (start, stop))
        self.start = start
        self.stop = stop
        self.tag = tag
    
    def __call__(self):
        return (self.start, self.stop, self.tag)
    
    def __repr__(self):
        return '(%d, %d, %s)' % (self.start, 
                                 self.stop, 
                                 self.tag)
    


def adapt_(entity):
    marks = []
    for _ in entity.matches:
        marks.append(Mark(
            _.span.start, 
            _.span.stop, 
            entity.tag
            ) 
        )
    return marks
    

from ipymarkup import(
        show_span_box_markup as show)
def show_markup(text, marks):
    show(text, [_() for _ in marks])


def shift_(marks, offset):
    for _ in marks:
        _.start -=offset 
        _.stop -=offset
    return marks 


def set_margin(head, tail):
    return (head.start, tail.stop)


def sorted_(marks):
     return sorted(marks, key=lambda _: _.start)

class NERpack():
    __attributes__ = ['entities', 'marks', 'margin']

    def __init__(self):
        self.marks = []
        self.entities = []
        self.margin = ()

    def add_marks(self, entities):
        for _ in entities:
            marks = adapt_(_)
            if not marks:
                continue
            self.marks += marks
            self.entities.append(_.label)
        
        if self.marks:
            self.marks = sorted_(self.marks)
            self.margin = set_margin(
                self.marks[0],
                self.marks[-1])

    def markstr(self):
        return ''.join(_.tag for _ in self.marks)
    
    def show(self, text):
        off_ = self.margin[0]
        _off = self.margin[1]
        show_markup(
            text[off_ : _off], 
            shift_(self.marks, off_)
        )
            
    def show_full(self, text):
        show_markup(text, self.marks)

