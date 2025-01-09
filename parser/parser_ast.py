from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

url = 'https://ast.ru/cat/khudozhestvennaya-literatura/'

def get_soup(url, page=1):
    #готовка супа
    reg = requests.get(url+f"?PAGEN_1={page}")
    reg.encoding = 'utf-8'
    return BeautifulSoup(reg.text, "lxml")


def get_url_book(url, page=1):
    #получаем список ссылок на книги
    soup = get_soup(url,page)
    url_books = []
    books = soup.find_all('a', class_='card__img-link')
    for i in books:
        url_books.append('https://ast.ru' + i.get('href'))
    return url_books

def get_data_books(url, max_pages=5):
    book_data = []
    for page in range(1, max_pages+1):
        print(f'Парсим страницу {page}...')
        book_links = get_url_book(url, page)
        if not book_links:
            print('Нет данных на этой странице, останавливаемся')
            break
        for link in book_links:
            #при переходе в карточку книг, нет пагинации
            reg = requests.get(link)
            reg.encoding = 'utf-8'
            soup = BeautifulSoup(reg.text, "lxml")

            title = soup.find('h1').text.strip()

            author = soup.find('a', class_='author-info__name')
            if author:
                author = author.get_text(strip=True)
            else:
                'None'

            annotation = soup.find('p', style='text-align: justify;')
            if annotation:
                annotation = annotation.get_text(strip=True)
            else:
                'None'

            num_of_pages = soup.find('div', class_='cover-info__text').find_all('b')[-2].text.strip()
            genre = soup.find_all('a', class_='breadcrumbs__link')[-1]
            series = soup.find('a', class_='book-detail__preview-characteristic-link').text.strip()
            book_cover = soup.find('picture', class_='book-carousel__main-image').find('img').get('src')
            book_data.append({
                'Title': title,
                'Author': author,
                'Annotation': annotation,
                'num of pages': num_of_pages,
                'genre': genre, 
                'series': series,
                'book cover': book_cover

            })
    return book_data


print(get_data_books(url, max_pages=1))


