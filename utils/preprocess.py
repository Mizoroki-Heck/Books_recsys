import pandas as pd
import os

def preprocess_data(data):
    if data is None:
        raise ValueError("Данные не были загружены корректно.")
     
    # data.drop('Unnamed: 0', axis=1, inplace=True)
    data = data.drop_duplicates(subset=['Title', 'Author'])
    data['Author'] = data['Author'].fillna('Без автора')
    data['Author'] = data['Author'].replace('<не указано>', 'Без автора')
    data['Annotation'] = data['Annotation'].fillna('Без аннотации')
    data['series'] = data['series'].fillna('Без серии')


    mask = data['num of pages'].str.contains('кг', case=False)
    data['num of pages'][mask]

    mask_audio = data['Title'].str.contains('Аудиокн.', case=False)
    data['Title'][mask_audio]
    data.drop(data[mask].index, inplace=True)
    data.drop(data[mask_audio].index, inplace=True)
    data.reset_index(inplace=True, drop=True)
    data['num of pages'] = data['num of pages'].astype('int')
    return data


