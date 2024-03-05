import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os

kimlik = UserAgent()
headers = kimlik.getRandom
target_url = "#"
visited_links = set()


def make_request(url):
    try:
        response = requests.get(url, headers,timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except (requests.RequestException, ValueError) as e:
        print(f"Hata: {e}")
        return None


def save_content(url, soup):
    h1_tag = soup.find('h1')
    if h1_tag:
        title = h1_tag.get_text().strip()
    else:
        title = "Başlık bulunamadı"

    paragraphs = soup.find_all('p')

    file_name = url.replace(target_url, '').strip('/').replace('/', '-') + ".txt"

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n\n")
        file.write("\n\n")
        for p in paragraphs:
            file.write(p.get_text().strip() + '\n')


def crawl(url):
    if url in visited_links:
        return

    soup = make_request(url)
    if soup is None:
        return

    visited_links.add(url)
    save_content(url, soup)

    for link in soup.find_all('a', href=True):
        found_link = link['href']
        if found_link.startswith('/'):
            found_link = target_url + found_link
        if target_url in found_link and found_link not in visited_links:
            crawl(found_link)


if __name__ == "__main__":
    crawl(target_url)
