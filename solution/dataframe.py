
from pandas import DataFrame, read_json


def get_label1():
    return "обеспечение исполнения контракта"

def get_label2():
    return "обеспечение гарантийных обязательств"




def cut_extracted(path):
    df = read_json(path)
    df.index = df['id']
    return df.drop(
        columns=['id', 'extracted_part'])


def extr_nested(path):
    from json import load
    file = open(path)
    dataJSON = load(file)
    file.close()

    df = DataFrame()
    x = 'extracted_part'
    for _ in dataJSON:
        dict = {
                'start': _[x]['answer_start'],
                'stop': _[x]['answer_end'],
                'search': _[x]['text']
        }
        from pandas import concat
        df = concat(
            [df, DataFrame(
                    dict, 
                    index=[_['id']])])

    return df 


def get_fulldf(path):
    return cut_extracted(path).join(
        extr_nested(path)
    )


def get_extrdf(path):
    df = get_fulldf(path)
    return df.drop(columns=['text'])




def switch_config(_, __):
    if _ and not __:
        return 'docs'
    if not _ and __:
        return 'answers'
    if _ and __:
        return 'full'
    return 0


def reads_json(
        path, 
        docs = True,
        extracted_part = True):

    config = switch_config(
        docs,
        extracted_part
    )
    
    if config == 'docs':
        return cut_extracted(path)
    if config == 'answers':
        return get_extrdf(path)
    if config == 'full':
        return get_fulldf(path)
    
    return DataFrame()   


