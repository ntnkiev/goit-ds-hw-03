import requests
from bs4 import BeautifulSoup
import re

# url = 'https://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span', class_='text')
# authors = soup.find_all('small', class_='author')
# tags = soup.find_all('div', class_='tags')
#
# for i in range(0, len(quotes)):
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#     break
url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
def get_urls():
    urls_list = []
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    content = soup.select('div[class=ajaxmonth] h4[class=normal] a')
    prefix = 'month.php? month='
    for link in content:
        url = prefix + re.search(r"\d{4}-\d{2}", link['href']).group()
        urls_list.append()

if __name__ == '__main__':
