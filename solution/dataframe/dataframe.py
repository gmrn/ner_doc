
from pandas import DataFrame, read_json


def extr_nested(path):
    df = read_json(path)
    return df.from_records(
        df['extracted_part']
    )


def cut_extracted(path):
    df = read_json(path).drop(
        columns=['extracted_part']
    )
    return df


def join_parts(path):
    
    part1 = cut_extracted(path)
    part2 = extr_nested(path)
    from pandas import concat
    return concat(
        [part1, part2], 
        axis=1
    ) 
    

def switch_config(_, __):
    if not (_ or __):
        return 'empty'
    if _ and __:
        return 'full'
    if _ and (not __):
        return 'docs'
    return ''


def reads_json(
        path, 
        docs = True,
        extracted_part = True):

    config = switch_config(
        docs,
        extracted_part
    )
    
    if config == 'empty':
        return DataFrame()
    if config == 'docs':
        return cut_extracted((path))
    if config == 'full':
        return join_parts(path)
    return extr_nested(path)   
