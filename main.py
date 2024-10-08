import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import time


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, folder='books/'):
    file_path = f'{folder}{filename}.txt'
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_image(book_image_url, book_url):
    file_name = book_image_url.split('/')[-1]
    file_path = f'img/{file_name}'
    img_url = urljoin(book_url, book_image_url)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    
def parse_book_page(book_response):
    soup = BeautifulSoup(book_response.text, 'lxml')
    book_image_url = soup.find('div', class_='bookimage').find('img')['src']
    comments = [comment.find(class_='black').text for comment in soup.find_all(class_='texts')]
    title_tag = soup.find('h1')
    title_text = title_tag.text
    title_text = title_text.split('::')
    autor = title_text[0].strip()
    book_name = title_text[1].strip()
    genres = soup.find('span', class_='d_book').find_all('a')
    book_genres = [genre.text for genre in genres]
    book = {
        'autor': autor, 
        'name': book_name, 
        'genre': book_genres, 
        'comments': comments,
        'image_url': book_image_url,
        }
    return book


def main():
    parser = argparse.ArgumentParser(
        description='Программа для скачивания книг'
    )
    parser.add_argument('--start_id', help='Id первой книги', type=int, default=1)
    parser.add_argument('--end_id', help='Id последней книги', type=int, default=10)
    args = parser.parse_args()

    Path("books").mkdir(parents=True, exist_ok=True)
    Path("img").mkdir(parents=True, exist_ok=True)
    url = "https://tululu.org/txt.php"
    for number in range(args.start_id, args.end_id+1):
        payload = {
            'id': number
        }
        book_url = f'https://tululu.org/b{number}/'
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            check_for_redirect(response)
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            book_parametrs = parse_book_page(book_response)
            download_txt(response, book_parametrs['name'])
            download_image(book_parametrs['image_url'], book_url)
        except requests.HTTPError:
            print('Такой книги нет')
        except requests.ConnectionError:
            print('Нет подключения к интернету')
            time.sleep(20)


if __name__ == '__main__':
    main()