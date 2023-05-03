
from yargy import rule, or_

from yargy.predicates import (
    eq, in_, 
    normalized, caseless
)

   
# CONTRACT
#     "обеспечение исполнения контракта"
#     "обеспечение исполнения настоящего контракта"
#     "обеспечение исполнения обязательств"
#     "обеспечения исполнения договора"
#     "обеспечение контракта"
#     "исполнение контракта"
#     "исполнение договора"
#     "обеспечение договора"


CONTRACT = rule(
    or_(
        normalized('обеспечение'),
        normalized('исполнение'),
    ).repeatable(),
    normalized('настоящий').optional(),
    or_(
        normalized('контракт'),
        normalized('договор'),
        normalized('обязательство')
    )
)

class Contract:
    rule = CONTRACT
    label = 'label1'
    tag = '1'



# GUARANTEE
#     "обеспечение гарантийных обязательств"
#     "обеспечение исполнения гарантийных обязательств"
#     "обеспечения исполнения обязательств"
#     "обеспечения исполнения контракта, гарантийных обязательств"
#     "обеспечения исполнения договора, гарантийных обязательств"
#     "обеспечения исполнения контракта (или) гарантийных обязательств"
#     "обеспечения исполнения договора (или) гарантийных обязательств"


BOUND = in_('()')

G_PART = rule(
    or_(
        normalized('контракт'),
        normalized('договор'),
    ).optional(),
    rule(
        BOUND.optional(),
        or_(
            eq(','),
            caseless('и'),
            caseless('или')
        ),
        BOUND.optional(),
    )
)


GUARANTEE = rule(
    or_(
        rule(normalized('обеспечение')),
        rule(normalized('исполнение'),)
    ).repeatable(),
    G_PART.optional(),
    or_(
        rule(normalized('гарантийный')),
        rule(normalized('обязательство'))
    ).repeatable(),
)

class Guarantee:
    rule = GUARANTEE
    label = 'label2'
    tag = '2'
