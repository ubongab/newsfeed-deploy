import requests
from bs4 import BeautifulSoup


class TopStories:

    def __init__(self):
        self.top = []
        self.top.extend(self._bbc())
        self.top.extend(self._metro())

    def _get_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    def _metro(self):
        soup = self._get_page('https://metro.co.uk/trending/')
        articles = soup.find(
            'div', class_='page-main col-ab').findAll('article')[:3]
        self.metro_trending = []
        for article in articles:
            title = article.find('h3').getText().strip()
            summary = article.find(
                'div', class_='nf-excerpt').getText().strip()
            url = article.find('a', class_="nf-image-link").get('href')
            img_url = article.find('img').get('src').split('?')[0]
            self.metro_trending.append({'title': title, 'summary': summary, 'link': url,
                                        'img_url': img_url, 'src': 'metro'})
        return self.metro_trending

    def _bbc(self):
        bbc = self._get_page('https://www.bbc.co.uk/news/uk')
        title = bbc.find(
            'div', class_="gel-layout__item gel-1/1").find('a').getText()
        img_url = bbc.find(
            'div', class_="gs-o-responsive-image gs-o-responsive-image--16by9 gs-o-responsive-image--lead").find('img').get('src')
        url = 'https://www.bbc.co.uk' + \
            bbc.find('div', class_="gel-layout__item gel-1/1").find('a').get('href')
        summary = bbc.find(
            'div', class_="gel-layout__item gel-1/1").find('p').getText()
        date_str = bbc.find(
            'div', class_="gel-layout__item gel-1/1").find('time').get('datetime')
        hrs_ago = bbc.find(
            'div', class_="gel-layout__item gel-1/1").find('time').find('span', class_='gs-u-vh').getText()
        return [{'title': title, 'summary': summary, 'link': url, 'img_url': img_url,
                 'date_str': date_str, 'hrs_ago': hrs_ago, 'src': 'bbc'}]


# top = TopStories()
# print(top.top)
