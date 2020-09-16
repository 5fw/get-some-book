import requests
import time
import lxml
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_content(target):
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    texts = bs.find('div', id='content')
    content = texts.text.strip().split('\xa0'*4)
    return content

if __name__ == '__main__':
    # server = (input("add a server html:"))
    # target = (input("add a target html:"))
    server = 'https://www.xsbiquge.com'
    target = 'https://www.xsbiquge.com/15_15338'
    book_name = 'book.txt'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    char_bs = BeautifulSoup(html, 'lxml')
    chapters = char_bs.find('div', id='list')
    chapters = char_bs.find_all('a')
    for chapter in tqdm(chapters):
        chapter_name = chapter.string
        url = server+chapter.get('href')

        if  '章' in chapter_name:
            content = get_content(url)
            with open(book_name, 'a', encoding='utf-8') as f:
                f.write(chapter_name)
                f.write('\n')
                f.write('\n'.join(content))
                f.write('\n')
