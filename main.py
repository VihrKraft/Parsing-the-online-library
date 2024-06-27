import requests
from pathlib import Path


Path("books").mkdir(parents=True, exist_ok=True)
for number in range(10):
    payload = {
        'id': number+1
    }
    url = f"https://tululu.org/txt.php"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    file_path = f'books/book{number+1}.txt'
    with open(file_path, 'wb') as file:
        file.write(response.content)
