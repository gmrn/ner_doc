
# from https://github.com/natasha/natasha/blob/09bf33ebfefe82e194439866d2d4cb67809fa173/natasha/extractors.py#L6

from yargy import Parser as YargyParser
from yargy.morph import MorphAnalyzer
from yargy.tokenizer import MorphTokenizer

from natasha.record import Record
from natasha import obj

class Parser(YargyParser):
    def __init__(self, rule, morph):
        # wraps pymorphy subclass
        # add methods check_gram, normalized
        # uses parse method that is cached
        morph = MorphAnalyzer(morph)

        tokenizer = MorphTokenizer(morph=morph)
        YargyParser.__init__(self, rule, tokenizer=tokenizer)


class Match(Record):
    __attributes__ = ['start', 'stop', 'fact']


def adapt_match(match):
    start, stop = match.span
    fact = match.fact.obj
    return Match(start, stop, fact)


class Extractor:
    def __init__(self, rule, morph):
        self.parser = Parser(rule, morph)

    def __call__(self, text):
        for match in self.parser.findall(text):
            yield adapt_match(match)

    def find(self, text):
        match = self.parser.find(text)
        if match:
            return adapt_match(match)


class AmountExtractor(Extractor):
    def __init__(self, morph):
        from .rules.amount import AMOUNT
        Extractor.__init__(self, AMOUNT, morph)


def get_amount_extractor():
    from natasha import MorphVocab
    return AmountExtractor(MorphVocab())