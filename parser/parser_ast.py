from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import time
import random
import os
from multiprocessing import Pool

url = 'https://ast.ru/cat/khudozhestvennaya-literatura/'

def get_soup(url, page=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://ast.ru/cat/khudozhestvennaya-literatura/',  # Здесь можно указать исходный URL
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    }
    #готовка супа
    reg = requests.get(url+f"?PAGEN_1={page}", headers=headers)
    reg.encoding = 'utf-8'
    return BeautifulSoup(reg.text, "lxml")

def logging(page, filename='progress.log'):
    with open(filename, 'w') as lg:
        lg.write(str(page))

def load_progress(filename='progress.log'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return int(f.read().strip())
    return 1

def get_url_book(url, page=1):
    #получаем список ссылок на книги
    soup = get_soup(url,page)
    url_books = []
    books = soup.find_all('a', class_='card__img-link')
    for i in books:
        url_books.append('https://ast.ru' + i.get('href'))
    return url_books

def save_to_csv(data, filename='books_data.csv'):
    file_exists = os.path.exists(filename)
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not file_exists, index=False)

def parse_book(link):
    reg = requests.get(link)
    time.sleep(random.randrange(2, 5))
    reg.encoding = 'utf-8'
    soup = BeautifulSoup(reg.text, "lxml")

    title = soup.find('h1').text.strip()

    author = soup.find('a', class_='book-detail__authors-item')
    author = author.get_text(strip=True) if author else "None"
    
    annotation = soup.find('p', style='text-align: justify;')
    annotation = annotation.get_text(strip=True) if annotation else "None"

    num_of_pages = soup.find('div', class_='cover-info__text')
    num_of_pages = num_of_pages.find_all('b')[-2].text.strip() if num_of_pages else "None"

    genre = soup.find_all('a', class_='breadcrumbs__link')[-1].text

    series = soup.find('a', class_='book-detail__preview-characteristic-link')
    series = series.text.strip() if series else "None"

    book_cover = soup.find('picture', class_='book-carousel__main-image')
    book_cover = book_cover.find('img').get('src') if book_cover else "None"


    return {
        'Title': title,
        'Author': author,
        'Annotation': annotation,
        'num of pages': num_of_pages,
        'genre': genre, 
        'series': series,
        'book cover': book_cover
    }


def get_data_books(url, max_pages, batch_size, filename='books_data'):
        book_data = []
        current_page = load_progress()
        for page in range(current_page, max_pages+1):
            try:
                print(f'Парсим страницу {page}...')
                book_links = get_url_book(url, page)
                time.sleep(random.randrange(2, 5))
                if not book_links:
                    print('Нет данных на этой странице, останавливаемся')
                    break

                with Pool(processes=12) as pool:
                    results = pool.map(parse_book, book_links)

                results = [r for r in results if r is not None]
                book_data.extend(results)

                if page % batch_size == 0:
                    print(f'Сохраняем промежуточные данные в файл: страница{page}')
                    logging(page)
                    save_to_csv(book_data, filename)
                    book_data.clear()

            except Exception as e:
                print(f"Ошибка при обработке книги на странице {page}: {e}")
                print('Продолжаем парсинг')
                continue
            
        if book_data:
            print(f"Сохраняем оставшиеся данные в файл")
            save_to_csv(book_data, filename)
    

if __name__ == '__main__':
    data = get_data_books(url, batch_size = 10, max_pages = 2500)




