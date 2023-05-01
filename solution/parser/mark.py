
class Mark():
    __attributes__ = ['start', 'stop', 'type']

    def __init__(self, start, stop, type = None):
        if start >= stop:
            raise ValueError('invert mark: (%r, %r)' % (start, stop))
        self.start = start
        self.stop = stop
        self.type = type
    
    def __repr__(self):
        return '(%d, %d, %s)' % (self.start, 
                                 self.stop, 
                                 self.type)
    
    def to_tuple(self):
        return (self.start, self.stop, self.type)
      



def get_label1():
    return "обеспечение исполнения контракта"

def get_label2():
    return "обеспечение гарантийных обязательств"



def get_matches(text, type):
    from .parser import select_parser
    return(
        select_parser(type).findall(text)
    ) 


def get_matches_(text):
    from .extractor import get_amount_extractor
    _ = get_amount_extractor()
    return _(text)


def normalize_marks(marks, type):
    pre_marks = []
    for mark in marks:
        pre_marks.append(Mark(
            mark.start, 
            mark.stop, 
            type))
    return pre_marks


def switch_(option):
    _ = {
        'label1' : '1',
        'label2' : '2',
        'additional': '+',
        'amount' : '₽',
    }
    return _[option]


def select_marks(text, type):
    type = switch_(type)
    if type == '₽':
        m_ = get_matches_(text)
        return [(Mark(_.start, _.stop, type)) for _ in m_]   
    
    m_ = get_matches(text, type)
    marks = [_.span for _ in m_]
    return normalize_marks(marks, type)


def sorted_(marks):
     return sorted(marks, key=lambda _: _.start)


def get_marks(text, 
              label = None,
              amount = False,
              additional = False):  
    _ = text

    marks = (
        select_marks(_, 'label1') 
        if label == get_label1() 
        else select_marks(_, 'label2'))

    if (amount):
        marks += select_marks(_, 'amount')
    if(additional):
        marks += select_marks(_, 'additional')
    
    return sorted_(marks)



def get_string(marks, label):
    marks_t = ''.join(_.type for _ in marks)


def get_bounds(text, label):
     marks = get_marks(text, label)
     return Mark(
          marks[0].start,
          marks[-1].stop,
     ) 


def select_part(text, label):
    bounds = get_bounds(text, label)
    return text[
        bounds.start:bounds.stop
    ]


def shift_marks(marks, bounds):
    offset = bounds.start
    for _ in marks:
         _.start += offset
         _.stop += offset
    return marks


def show_markup(text, marks, bounds=None):
    from ipymarkup import(
        show_span_box_markup 
        as show
    )
    show(text, (_.to_tuple() for _ in marks))

