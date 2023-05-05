
# using https://github.com/natasha/natasha/blob/09bf33ebfefe82e194439866d2d4cb67809fa173/natasha/grammars/money.py
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
    

class Currency:
    RUBLES = 'RUB'
    DOLLARS = 'USD'
    EURO = 'EUR'
    PERCENT= 'PER'


DOT = eq('.')
INT = type('INT')


########
#
#   CURRENCY
#
##########


EURO = rule(
    or_(
        normalized('евро'),
        eq('€')
    )
)

DOLLARS = rule(
    or_(
        normalized('доллар'),
        eq('$')
    )
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
)

PERCENT = rule(
    or_(
        normalized('процент'),
        eq('%')   
    )
)

CURRENCY = or_(
    RUBLES,
    PERCENT,
    EURO,
    DOLLARS,
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
)
