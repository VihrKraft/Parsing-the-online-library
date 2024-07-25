import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, folder='books/'):
    file_path = f'{folder}{filename}.txt'
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_image(book_url):
    book_image_url = soup.find('div', class_='bookimage').find('img')['src']
    file_name = book_image_url.split('/')[-1]
    file_path = f'img/{file_name}'
    book_image_url = urljoin(book_url, book_image_url)
    response = requests.get(book_image_url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    
    



Path("books").mkdir(parents=True, exist_ok=True)
Path("img").mkdir(parents=True, exist_ok=True)
url = "https://tululu.org/txt.php"
for number in range(1, 11):
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
        soup = BeautifulSoup(book_response.text, 'lxml')
        title_tag = soup.find('h1')
        title_text = title_tag.text
        title_text = title_text.split('::')
        autor = title_text[0].strip()
        book_name = title_text[1].strip()
        download_txt(response, book_name)
        download_image(book_url)
    except requests.HTTPError:
        print('Такой книги нет')
