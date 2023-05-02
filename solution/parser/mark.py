
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


def find_matches(text, types):
    marks = []
    from .parser import parse_text
    for t in types:
        matches = parse_text(text, t)
        marks += normalize_(matches, t)
    return marks


def normalize_(marks, type):
    prepared_ = []
    for m_ in marks:
        try:
            prepared_.append(Mark(
                m_.span.start, 
                m_.span.stop, 
                type))
        except:
            prepared_.append(Mark(
                m_.start, 
                m_.stop, 
                type))
    return prepared_


def sorted_(marks):
     return sorted(marks, key=lambda _: _.start)


def switch_label(label):
    return '1' if label == get_label1() else '2'


def find_marks(text, 
              label = None,
              amount = True,
              additional = True):  
    types = []

    types.append(switch_label(label))
    if (amount):
        types.append('₽')
    if(additional):
        types.append('A')

    marks = find_matches(text, types)
    return sorted_(marks)


def encode_marks(marks):
    return ''.join(_.type for _ in marks).replace('2', '1')


def find_entry(enc_):
    import re
    arr = [_.start() for _ in re.finditer(
        '1A₽', enc_)]
    arr += [_.start() for _ in re.finditer(
        'A1₽', enc_)]
    return arr

def find_entry_(enc_):
    import re
    return [_.start() for _ in re.finditer('₽', enc_)]
    


def get_entry(marks):
    return find_entry(encode_marks(marks))

def get_entry_(marks):
    return find_entry_(encode_marks(marks))


def get_offset(text, label):    
    type = switch_label(label)
    
    from .parser import select_parser
    span = select_parser(type).find(text)
    _ = span.span.start
    try:
        span = select_parser('A').find(text)
        __ = span.span.start
        return min(_, __)
    except:
        return _  


def shift_marks(marks, bounds):
    offset = bounds.start
    for _ in marks:
         _.start += offset
         _.stop += offset
    return marks


def show_markup(text, marks):
    from ipymarkup import(
        show_span_box_markup 
        as show
    )
    show(text, (_.to_tuple() for _ in marks))

