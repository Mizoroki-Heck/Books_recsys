from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db import get_data_db 
import re

app = Flask(__name__)

data_books = get_data_db('SELECT * FROM books')
data_lsa = get_data_db('SELECT * FROM lsa')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        books_users = request.form['bookTitle']
        author_users = request.form['authorName']
        author_split = author_users.split()

        pattern_1 = re.compile(fr'(?i){re.escape(author_split[0])}\s{re.escape(author_split[1])}')
        pattern_2 = re.compile(fr'(?i){re.escape(author_split[1])}\s{re.escape(author_split[0])}')

        try:
            filtered_data = data_books[
                (data_books['Title'] == books_users) &
                (data_books['Author'].str.contains(pattern_1) | data_books['Author'].str.contains(pattern_2))
            ].index[0]
        except IndexError:
            return "Книга или автор не найдены."
        
        similiar_books = cosine_similarity(data_lsa.iloc[filtered_data].to_numpy().reshape(1, -1), data_lsa.to_numpy())
        list_similiar = list(enumerate(similiar_books[0]))
        sorted_similiar = sorted(list_similiar, key=lambda x: x[1], reverse=True)

        top5 = sorted_similiar[1:6]
        other_books = [book for book in list_similiar if book[1] > 0.5 and book[1] < 0.8][:15]

        return render_template('index.html',data=data_books, books=top5, other_books=other_books)
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
