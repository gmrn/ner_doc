from .label import CONTRACT, GUARANTEE
from .amount import AMOUNT
from .custom import(
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