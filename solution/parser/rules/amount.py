
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


class Currency:
    RUBLES = 'RUB'
    DOLLARS = 'USD'
    EURO = 'EUR'
    PERCENT= 'PER'


Money = fact(
    'Money',
    ['integer', 'fraction', 'multiplier', 'currency', 'coins']
)


class Money(Money):
    @property
    def amount(self):
        amount = self.integer
        if self.fraction:
            amount += self.fraction / 100
        if self.multiplier:
            amount *= self.multiplier
        if self.coins:
            amount += self.coins / 100
        return amount

    @property
    def obj(self):
        from natasha import obj
        return obj.Money(self.amount, self.currency)


DOT = eq('.')
INT = type('INT')


########
#
#   CURRENCY
#
##########


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

RUBLES = or_(
    rule(
        normalized('российский').optional(),
        normalized('рубль')
    ),
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

PERCENT = or_(
    normalized('процент'),
    eq('%')   
).interpretation(
    const(Currency.PERCENT)
)

CURRENCY = or_(
    RUBLES,
    PERCENT,
    EURO,
    DOLLARS,
).interpretation(
    Money.currency
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


############
#
#  MULTIPLIER
#
##########


MILLIARD = or_(
    rule(caseless('млрд'), DOT.optional()),
    rule(normalized('миллиард'))
).interpretation(
    const(10**9)
)

MILLION = or_(
    rule(caseless('млн'), DOT.optional()),
    rule(normalized('миллион'))
).interpretation(
    const(10**6)
)

THOUSAND = or_(
    rule(caseless('т'), DOT),
    rule(caseless('тыс'), DOT.optional()),
    rule(normalized('тысяча'))
).interpretation(
    const(10**3)
)

MULTIPLIER = or_(
    MILLIARD,
    MILLION,
    THOUSAND
).interpretation(
    Money.multiplier
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
        'нуль',
        'один'
    }),
    DOT
)

MODIFIER = in_caseless({
    'целых',
    'сотых',
    'десятых'
})

PART = or_(
    rule(
        or_(
            eq('_'),
            INT,
            NUMR,
            MODIFIER,
        )
    ),
    MILLIARD,
    MILLION,
    THOUSAND,
    CURRENCY,
    COINS_CURRENCY,
    # PERCENT
)

BOUND = rule(in_('()//'))

NUMERAL = rule(
    BOUND.optional(),
    PART.repeatable(),
    BOUND.optional(),
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
).interpretation(
    Money.integer.custom(normalize_integer)
)

FRACTION = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
).interpretation(
    Money.fraction.custom(normalize_fraction)
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
).interpretation(
    Money.coins.custom(int)
)

COINS_AMOUNT = rule(
    COINS_INTEGER,
    NUMERAL.optional()
)


#########
#
#   AMOUNT
#
###########


AMOUNT = rule(
    or_(
        rule(
            VALUE,
            CURRENCY
        ),
        rule(
            CURRENCY,
            VALUE
        ),
    ),
    # and_(
    #     VALUE,
    #     CURRENCY
    # ),
    COINS_AMOUNT.optional(),
    COINS_CURRENCY.optional()
).interpretation(
    Money
)