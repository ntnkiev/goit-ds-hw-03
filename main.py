import requests
from bs4 import BeautifulSoup
import json

URL = "https://quotes.toscrape.com"


def page_scrape(url, authors, quotes) -> str | None:
    # функція скрапінгу сторінки about автора
    def authors_scrape(authors_url, authors):
        response = requests.get(authors_url)
        soup = BeautifulSoup(response.text, 'lxml')
        fullname = soup.find("h3", class_="author-title").get_text().strip()
        born_date = soup.find("span", class_="author-born-date").get_text().strip()
        born_location = soup.find("span", class_="author-born-location").get_text().strip()
        description = soup.find("div", class_="author-description").get_text().strip()
        # заповнення списку авторів
        authors.append(
            {"fullname": fullname, "born_date": born_date, "born_location": born_location, "description": description})

    # скрапінг сторінки цитат
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    page_quotes = soup.find_all('span', class_='text')
    page_authors = soup.find_all('small', class_='author')
    page_tags = soup.find_all('div', class_='tags')
    page_about = soup.select("[href^='/author']")  # формування лінка сторінки автора
    for a in page_about:
        authors_url = URL + a['href']
        authors_scrape(authors_url, authors)  # виклик функції скрапінгу сторінки about автора

    for i in range(0, len(page_quotes)):  # заповнення списку цитат
        tag_list = []
        tagsforquote = page_tags[i].find_all('a', class_='tag')
        for tagforquote in tagsforquote:
            tag_list.append(tagforquote.text)
        quotes.append({"tags": tag_list, "author": page_authors[i].text, "quote": page_quotes[i].text})

    next_url = soup.find('li', class_='next')  # пошук посилання на наступну сторінку
    if not next_url:
        return None
    next_url = URL + next_url.find('a')['href']
    # print(next_url)
    return next_url


if __name__ == "__main__":
    authors = []
    quotes = []
    new_url = URL
    while True:  # перебір всіх сторінок
        new_url = page_scrape(new_url, authors, quotes)
        if not new_url:
            break

    # Збереження даних у файли JSON
    with open("quotes.json", "w", encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False, indent=4)

    with open("authors.json", "w", encoding='utf-8') as file:
        json.dump(authors, file, ensure_ascii=False, indent=4)
