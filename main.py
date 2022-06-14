import requests
import bs4
from fake_headers import Headers


def get_urls(url, HEADERS, base_url):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles_links = soup.find_all(class_="tm-article-snippet__title-link")
    links = [article.attrs['href'] for article in articles_links]
    urls = [base_url + link for link in links]
    return urls


def get_info(urls, headers, keywords):
    for url in urls:
        response = requests.get(url, headers=headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article')
        for article in articles:
            for version in range(1, 3):
                try:
                    head = article.find(class_=f'article-formatted-body article-formatted-body article-formatted-body_version-{version}')
                    words_list = head.text.strip().split(' ')
                    if set(words_list) & set(keywords):
                        time = article.find('time').attrs['title']
                        title = article.find('h1').find('span').text
                        print(f'{time} - {title} - {url}')
                except AttributeError:
                    continue


def main():
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'
    KEYWORDS = ['урок', 'сайты', 'web', 'Data', 'платформа', 'Swift']
    HEADERS = Headers(os='win', headers=True).generate()
    urls = get_urls(url, HEADERS, base_url)
    get_info(urls, HEADERS, KEYWORDS)


if __name__ == '__main__':
    main()