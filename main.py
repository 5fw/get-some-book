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
    # search book name
    inputKeyword = (input("输入书名:"))
    # server base URl
    searchUrl = "https://www.xsbiquge.com/search.php"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    searchParams = {
        'keyword' :inputKeyword
    }
    # request then filter useful data
    req = requests.get(searchUrl, headers=header, params=searchParams)
    req.encoding = "utf-8"
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    bookListInfo = bs.find_all('a', 'result-game-item-title-link')
    bookInfo = []
    count = 0
    # append new array get book name and download url
    for list in bookListInfo:
        bookInfo.append([count, list['title'], list['href']])
        count+=1
    for formatList in bookInfo:
        print(formatList[0],'.',formatList[1])
    # select book
    inputBookNumber = int((input("输入序号:")))
    # combine into a file name
    bookName = bookInfo[inputBookNumber][1]+'.txt'
    selectBookUrl = bookInfo[inputBookNumber][2]
    # base server url
    server = 'https://www.xsbiquge.com'
    req = requests.get(url=selectBookUrl)
    req.encoding = 'utf-8'
    html = req.text
    char_bs = BeautifulSoup(html, 'lxml')
    # filter
    # chapters = char_bs.find('div', id='list')
    chapters = char_bs.find_all('a')
    for chapter in tqdm(chapters):
        chapter_name = chapter.string
        url = server+chapter.get('href')
        # remove useless chapter,only keep chapter name in '章'
        if  '章' in chapter_name:
            content = get_content(url)
            with open(bookName, 'a', encoding='utf-8') as f:
                f.write(chapter_name)
                f.write('\n')
                f.write('\n'.join(content))
                f.write('\n')
