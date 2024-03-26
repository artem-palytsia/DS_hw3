import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання даних про цитати зі сторінки
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all(class_='quote')

    scraped_quotes = []
    for quote in quotes:
        text = quote.find(class_='text').get_text()
        author = quote.find(class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        scraped_quotes.append({
            "quote": text,
            "author": author,
            "tags": tags
        })
    return scraped_quotes

# Функція для отримання даних про авторів зі сторінки
def scrape_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    authors = soup.select('.author + a')

    scraped_authors = {}
    for author in authors:
        author_name = author.get_text()
        author_page_url = 'http://quotes.toscrape.com' + author['href']
        author_response = requests.get(author_page_url)
        author_soup = BeautifulSoup(author_response.text, 'html.parser')
        born_date = author_soup.find(class_='author-born-date').get_text()
        born_location = author_soup.find(class_='author-born-location').get_text()
        description = author_soup.find(class_='author-description').get_text()
        scraped_authors[author_name] = {
            "fullname": author_name,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }
    return scraped_authors

# Головна функція
def main():
    base_url = 'http://quotes.toscrape.com'
    quotes_url = base_url + '/page/1/'
    all_quotes = []

    # Збираємо цитати з усіх сторінок
    while quotes_url:
        quotes = scrape_quotes(quotes_url)
        all_quotes.extend(quotes)
        next_page_link = BeautifulSoup(requests.get(quotes_url).text, 'html.parser').find(class_='next')
        quotes_url = base_url + next_page_link.find('a')['href'] if next_page_link else None

    # Збираємо дані про авторів
    authors_data = scrape_authors(base_url)

    # Записуємо дані у файли JSON
    with open('quotes.json', 'w') as quotes_file:
        json.dump(all_quotes, quotes_file, indent=2)

    with open('authors.json', 'w') as authors_file:
        json.dump(list(authors_data.values()), authors_file, indent=2)

if __name__ == "__main__":
    main()
