
import re

from yargy import (
    rule,
    and_, or_,
)

from yargy.predicates import (
    eq, length_eq,
    in_, in_caseless,
    gram, type,
    normalized, caseless, dictionary
)


DOT = eq('.')
INT = type('INT')


########
#
#   SIGN
#
##########


SIGN = or_(
    normalized('процент'),
    eq('%')
)


########
#
#  NUMERAL
#
#######


NUMR = or_(
    gram('NUMR'),
    dictionary({
        'ноль',
        'один'
    }),
)

MODIFIER = in_caseless({
    'целых',
    'сотых',
    'десятых'
})

PART = or_(
    INT,
    NUMR,
    MODIFIER,


    SIGN
)

BOUND = in_('()//')

NUMERAL = rule(
    BOUND,
    PART.repeatable(),
    BOUND
)


#######
#
#   AMOUNT
#
########


def normalize_integer(value):
    integer = re.sub(r'[\s.,]+', '', value)
    return int(integer)


def normalize_fraction(value):
    fraction = value.ljust(2, '0')
    return int(fraction)


PART = and_(
    INT,
    length_eq(3)
)

SEP = in_(',.')

INTEGER = or_(
    rule(INT),
    rule(INT, PART),
    rule(INT, PART, PART),
    rule(INT, SEP, PART),
    rule(INT, SEP, PART, SEP, PART),
)

FRACTION = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
)

AMOUNT = rule(
    INTEGER,
    rule(
        SEP,
        FRACTION
    ).optional(),
    NUMERAL.optional()
)


#########
#
#   PERCENT
#
###########


PERCENT = rule(
    AMOUNT,
    SIGN
)