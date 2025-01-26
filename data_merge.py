import pandas as pd
books_data = pd.read_csv(r'dataset\books_data')
anno_data = pd.read_csv(r'dataset\annotation_data.csv')

#удалим дубликаты и сбросим индекс т.е номера не соответствуют
books_data = books_data.drop_duplicates(subset=['Title', 'Author'])
anno_data = anno_data.drop_duplicates(subset=['Title', 'Author'])

books_data.reset_index(inplace=True)
books_data.drop('index', axis=1, inplace=True)
anno_data.reset_index(inplace=True)
anno_data.drop('index', axis=1, inplace=True)

#Соединим два датасета по Названию и авторам
merged_df = books_data.merge(anno_data, on=['Title', 'Author'], how='left', suffixes=('', '_df2'))
#заполним пропуски первого датафрейма, значениями из второго
merged_df['Annotation'] = merged_df['Annotation'].fillna(merged_df['Annotation_df2'])
merged_df.drop('Annotation_df2', axis=1, inplace=True)

#сохраним csv
merged_df.to_csv('dataset/merged_data_books.csv')