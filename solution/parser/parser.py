
from .rules.label import(
    CONTRACT,
    GUARANTEE
)
from .rules.additional import(
    ADDITIONAL
)


def switch_parser(type):
    switch = {
        '1' : CONTRACT,
        '2' : GUARANTEE,
        '+' : ADDITIONAL,
    }
    return switch[type]


def select_parser(type):
    RULE = switch_parser(type)
    from yargy import Parser
    return Parser(RULE)
    


