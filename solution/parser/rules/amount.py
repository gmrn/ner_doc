
# using https://github.com/natasha/natasha/blob/09bf33ebfefe82e194439866d2d4cb67809fa173/natasha/grammars/money.py

import re

from yargy import (
    rule,
    and_, or_,
)

from yargy.interpretation import (
    fact,
    const
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
#   CURRENCY
#
##########

class Currency:
    RUBLES = 'RUB'
    DOLLARS = 'USD'
    EURO = 'EUR'

EURO = or_(
    normalized('евро'),
    eq('€')
).interpretation(
    const(Currency.EURO)
)

DOLLARS = or_(
    normalized('доллар'),
    eq('$')
).interpretation(
    const(Currency.DOLLARS)
)

REGION = rule(
    normalized('российский')
)

RUBLES = or_(
    REGION.optional(),  
    rule(normalized('рубль')),
    rule(
        or_(
            caseless('руб'),
            caseless('р'),
            eq('₽')
        ),
        DOT.optional()
    )
).interpretation(
    const(Currency.RUBLES)
)

CURRENCY = or_(
    EURO,
    DOLLARS,
    RUBLES
)

KOPEIKA = or_(
    rule(normalized('копейка')),
    rule(
        or_(
            caseless('коп'),
            caseless('к')
        ),
        DOT.optional()
    )
)

CENT = or_(
    normalized('цент'),
    eq('¢')
)

EUROCENT = normalized('евроцент')

COINS_CURRENCY = or_(
    KOPEIKA,
    rule(CENT),
    rule(EUROCENT)
)


########
#
#   SIGN
#
##########


SIGN = or_(
    rule(normalized('процент')),
    rule(eq('%'))   
)


############
#
#  MULTIPLIER
#
##########


MILLIARD = or_(
    rule(caseless('млрд'), DOT.optional()),
    rule(normalized('миллиард'))
)

MILLION = or_(
    rule(caseless('млн'), DOT.optional()),
    rule(normalized('миллион'))
)

THOUSAND = or_(
    rule(caseless('т'), DOT),
    rule(caseless('тыс'), DOT.optional()),
    rule(normalized('тысяча'))
)

MULTIPLIER = or_(
    MILLIARD,
    MILLION,
    THOUSAND
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

PART_MONEY = or_(
    MILLIARD,
    MILLION,
    THOUSAND,
    CURRENCY,
    COINS_CURRENCY
)

PART = rule(
    or_(
        INT,
        NUMR,
        MODIFIER
    ),
    or_(
        PART_MONEY,
        SIGN
    )
)

BOUND = in_('()//')

NUMERAL = rule(
    BOUND,
    PART.repeatable(),
    BOUND
)


#######
#
#   VALUE
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

VALUE = rule(
    INTEGER,
    rule(
        SEP,
        FRACTION
    ).optional(),
    MULTIPLIER.optional(),
    NUMERAL.optional()
)

COINS_INTEGER = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
)

COINS_VALUE = rule(
    COINS_INTEGER,
    NUMERAL.optional()
)


#########
#
#   MONEY
#
###########


MONEY = rule(
    VALUE,
    CURRENCY,
    COINS_VALUE.optional(),
    COINS_CURRENCY.optional()
)


#########
#
#   PERCENT
#
###########


PERCENT = rule(
    VALUE,
    SIGN
)


#########
#
#   AMOUNT
#
###########


AMOUNT = or_(
    MONEY,
    PERCENT
)