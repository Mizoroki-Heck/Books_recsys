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

def get_last_page(url):
    soup = get_soup(url)
    last_page = soup.find_all('a', class_='pagination__link')[-2].text
    return int(last_page)  # Возвращаем число, чтобы его можно было использовать дальше

last_page = get_last_page(url)

def logging(page, filename='progress_annotation.log'):
    with open(filename, 'w') as lg:
        lg.write(str(page))

def load_progress(filename='progress_annotation.log'):
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

def save_to_csv(data, filename='annotation_data.csv'):
    os.makedirs('dataset', exist_ok=True)
    filepath = os.path.join('dataset', filename)

    file_exists = os.path.exists(filepath)
    df = pd.DataFrame(data)
    df.to_csv(filepath, mode='a', header=not file_exists, index=False)

def parse_book(link):
    try:
        reg = requests.get(link)
        time.sleep(random.randrange(2, 5))
        reg.encoding = 'utf-8'
        soup = BeautifulSoup(reg.text, "lxml")

        title = soup.find('h1').text.strip()

        annotation = soup.find('p', style='text-align: justify;')
        if annotation:
            annotation = annotation.get_text(strip=True)
        else:
            text_div = soup.find('div', class_='text')
            if text_div:
                annotation = text_div.get_text(separator='\n', strip=True)
            else:
                annotation = None
                print('Ничего не нашел')

        return {
            'Title': title,
            'Annotation': annotation
        }
    except Exception as e:
        print(f"Ошибка при обработке книги: {link}\nОшибка: {e}")
        return None

def get_data_books(url, max_pages, batch_size, filename='annotation_data.csv'):
        book_data = []
        current_page = load_progress()
        for page in range(current_page, max_pages+1):
            try:
                print(f'Парсим страницу {page}/{max_pages}')
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
    data = get_data_books(url, batch_size = 10, max_pages = last_page)




