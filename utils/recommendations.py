from db import get_data_db
from db import load_to_db

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD

import pandas as pd


def lsa_calculation_save_to_sql():
    data = get_data_db('SELECT * FROM books')
    
    features = (data['Author'] + ' ' + data['genre'] + ' ' + data['series'] + ' ' + data['Annotation'])
    vectorizer = CountVectorizer()
    bag_of_words = vectorizer.fit_transform(features)

    tfidf_transformer = TfidfTransformer()
    tfidf = tfidf_transformer.fit_transform(bag_of_words)

    lsa_transform = TruncatedSVD(n_components=100, algorithm='arpack')
    lsa = lsa_transform.fit_transform(tfidf)

    df = pd.DataFrame(lsa)
    load_to_db(df,'lsa', 'replace')


