from parser_ast import get_data_books
from preprocess import clear_df, preprocess_data
from db import load_to_db

import pandas as pd

url = 'https://ast.ru/cat/khudozhestvennaya-literatura/'

def etl(url):
    data = get_data_books(url)
    print('✅Данные собраны')
    cleaned_data = preprocess_data(data)
    print('✅Данные обработаны')
    load_to_db(cleaned_data)
    print('✅ETL отработал')
    clear_df()
    

if __name__ == '__main__':
    etl(url)