
from yargy.pipelines import morph_pipeline

ADDITION = morph_pipeline([
    'сумма',
    'размер'
])

class Addition:
    rule = ADDITION
    label = 'addition'
    tag = '+'