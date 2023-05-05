
import sys
from pandas import(
    DataFrame, 
    read_json, 
    concat)


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
    _ = 'extracted_part'
    for row in dataJSON:
        dict = {
                'start': row[_]['answer_start'],
                'stop': row[_]['answer_end'],
                'search': row[_]['text']
        }
        df = concat([df, DataFrame(dict, index=[row['id']])])
    return df 


def main() -> int:
    path = 'data/train.json'
    
    cut_extracted(path).to_csv('data/train.csv')
    extr_nested(path).to_csv('data/target.csv')
    return 0

if __name__ == '__main__':
    main()

