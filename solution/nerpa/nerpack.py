
class Mark():
    __attributes__ = ['start', 'stop', 'content', 'tag']

    def __init__(self, start, stop, content= None, tag = None):
        if start >= stop:
            raise ValueError('invert mark: (%r, %r)' % (start, stop))
        self.start = start
        self.stop = stop
        self.content = content
        self.tag = tag
    
    def __call__(self):
        return (self.start, self.stop, self.tag)
    
    def __repr__(self):
        return '(%d, %d, %r, %r)' % (self.start, 
                                    self.stop,
                                    self.content, 
                                    self.tag)
    

def parse_(marks, text):
    for _ in marks:
        _.content = text[_.start:_.stop]
    return marks 


def extract_(entity, text):
    marks = []
    for _ in entity.matches:
        marks.append(Mark(
            start=_.span.start, 
            stop=_.span.stop,
            tag=entity.tag
            ) 
        )
    if text:
        return parse_(marks=marks, text=text)
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


def sorted_(marks):
     return sorted(marks, key=lambda _: _.start)


def unpack_(entities, text):
    marks=[] 
    labels=[] 
    margins=[]
    
    for _ in entities:
            marks += extract_(entity=_, text=text)
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


def adapt_(matches, text):
    marks = []
    for _ in matches:
        marks.append(Mark(_[0], _[1]))
    marks = sorted_(marks)
    if text:
        return parse_(marks=marks, text=text)
    return marks


class NERpack():
    __attributes__ = ['entities', 'marks', 'margins']

    def __init__(self):
        self.marks = self.labels = self.margins = []  
        
    def add_marks(self, 
                  entities=None, 
                  matches=None, 
                  text=None):
        if entities:
            pack = unpack_(entities, text)
            self.marks = pack['marks']
            self.entities = pack['labels']
            self.margins = pack['margins']
        if matches:
            ### !!!!set margins
            self.marks = adapt_(matches, text)

    def markstr(self):
        return ''.join(_.tag for _ in self.marks)

    def show(self, text):
        start = self.margins[0]
        stop = self.margins[1]
        marks = shift_(
            marks=self.marks, offset=start)
        show_markup(
            text=text[start : stop], 
            marks=marks)
            
    def show_full(self, text):
        show_markup(text, self.marks)

