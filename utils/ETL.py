from parser_ast import get_data_books
from preprocess import preprocess_data
from recommendations import lsa_calculation_save_to_sql
from db import load_to_db

import pandas as pd

url = 'https://ast.ru/cat/khudozhestvennaya-literatura/'

def etl(url):
    data = get_data_books(url)
    print('✅Данные собраны')
    cleaned_data = preprocess_data(data)
    print('✅Данные обработаны')
    load_to_db(cleaned_data, 'books', 'append')
    print('✅Данные с книгами дополнены')
    lsa_calculation_save_to_sql()
    print('✅Lsa матрица посчитана, и загружена в бд')
    print('✅ETL отработал')
    
if __name__ == '__main__':
    etl(url)