from .entities.label import CONTRACT, GUARANTEE
from .entities.amount import AMOUNT
from .entities.custom import(
    ADDITION
)

class Contract:
    rule = CONTRACT
    label = 'label1'
    tag = '1'

class Guarantee:
    rule = GUARANTEE
    label = 'label2'
    tag = '2'

class Amount:
    rule = AMOUNT
    label = 'amount'
    tag = '₽'


class Addition:
    rule = ADDITION
    label = 'addition'
    tag = 'ADD'