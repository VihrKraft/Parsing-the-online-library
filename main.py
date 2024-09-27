import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse


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
    book_image_url = urljoin(book_url, book_image_url)
    response = requests.get(book_image_url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    
def parse_book_page(book_url):
    book_response = requests.get(book_url)
    book_response.raise_for_status()
    soup = BeautifulSoup(book_response.text, 'lxml')
    book_image_url = soup.find('div', class_='bookimage').find('img')['src']
    comments = soup.find_all(class_='texts')
    for comment in comments:
        comment = comment.find(class_='black')
        comment = comment.text
    title_tag = soup.find('h1')
    title_text = title_tag.text
    title_text = title_text.split('::')
    autor = title_text[0].strip()
    book_name = title_text[1].strip()
    genres = soup.find('span', class_='d_book').find_all('a')
    book_genres = []
    for genre in genres:
        book_genres.append(genre.text)
    book = {
        'Автор': autor, 
        'Название': book_name, 
        'Жанр': book_genres, 
        'Комментарии': comments,
        'Ссылка на изображение': book_image_url,
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
            parse_book = parse_book_page(book_url)
            download_txt(response, parse_book['Название'])
            download_image(parse_book['Ссылка на изображение'], book_url)
        except requests.HTTPError:
            print('Такой книги нет')


if __name__ == '__main__':
    main()