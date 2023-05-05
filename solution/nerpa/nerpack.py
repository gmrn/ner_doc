
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
    

def sorted_(marks):
     return sorted(marks, key=lambda _: _.start)


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

def unpack_(entities):
    marks=[] 
    labels=[] 
    margins=[]
    
    for _ in entities:
            marks += adapt_(entity=_)
            labels.append(_.label)
    if marks:
        marks = sorted_(marks)
        margins = (
            marks[0].start,
            marks[-1].stop)

    return {'marks' : marks, 
            'labels' : labels, 
            'margins' : margins
            }


class NERpack():
    __attributes__ = ['entities', 'marks', 'margins']

    def __init__(self, entities):
        if entities:
            pack = unpack_(entities=entities)
            self.marks = pack['marks']
            self.entities = pack['labels']
            self.margins = pack['margins']

    def markstr(self):
        return ''.join(_.tag for _ in self.marks)
    
    def show(self, text):
        start = self.margins[0]
        stop = self.margins[1]
        marks = shift_(marks=self.marks, offset=start)
        show_markup(
            text=text[start : stop], 
            marks=marks)
            
    def show_full(self, text):
        show_markup(text, self.marks)

