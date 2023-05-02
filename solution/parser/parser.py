
from .rules.label import(
    CONTRACT,
    GUARANTEE
)
from .rules.amount import(
    AMOUNT
)
from .rules.additional import(
    ADDITIONAL
)


def switch_parser(type):
    switch = {
        '1' : CONTRACT,
        '2' : GUARANTEE,
        '₽' : AMOUNT,
        'A' : ADDITIONAL,
    }
    return switch[type]


def select_parser(type):
    RULE = switch_parser(type)
    from yargy import Parser
    return Parser(RULE)


def parse_text(text, type):
    parser = select_parser(type)
    from .extractor import extract_money
    return parser.findall(text) if type != '₽' else extract_money(text)


