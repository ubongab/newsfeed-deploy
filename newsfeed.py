import feedparser
from dateutil import parser
import pandas as pd


class NewsFeed:
    # categories = ['education', 'health', 'politics', 'technology', 'business']
    bbc = 'http://feeds.bbci.co.uk/news/{}/rss.xml'
    indepedent = 'http://www.independent.co.uk/rss'
    sun = 'https://www.thesun.co.uk/feed/'
    daily_express = 'http://feeds.feedburner.com/daily-express-{}'
    channel4 = 'https://www.channel4.com/news/{}/feed'
    # huffington_post = 'https://www.huffingtonpost.co.uk/feeds/index.xml'
    standard = 'https://www.standard.co.uk/rss'
    wired = 'https://www.wired.co.uk/feed/rss'
    mirror = 'https://www.mirror.co.uk/?service=rss'
    sky = 'http://feeds.skynews.com/feeds/rss/{}.xml'

    urls = {'bbc': bbc, 'independent': indepedent,
            'sun': sun, 'daily_express': daily_express, 'channel4': channel4,
            'standard': standard, 'wired': wired, 'mirror': mirror, 'sky': sky}

    def _get_feed(self, url: str, src=None, category=None):
        '''
        ## Parameters:
            url: str - newsfeed url
            src: None or str - news source e.g. bcc
            category: str - news category e.g. politics
        ## Returns:
            list: of dictionaries with e.g. {title,summary, datetime,date_str, tags, src}
            src: None or str - news source e.g. bcc
            category: str - news category e.g. politics
        '''
        self.items = []
        d = feedparser.parse(url)
        for i in d.entries:
            title = i.title
            link = i.link
            datetime_ = parser.parse(i.published)
            date_str = i.published
            try:
                summary = i.summary
                if summary is None:
                    summary = i.description
            except:
                summary = ''
            try:
                tags = [t.term.lower() for t in i.tags]
            except:
                if category is not None:
                    tags = category
                else:
                    tags = ['']

            self.items.append({'title': title, 'summary': summary,
                              'link': link, 'date_str': date_str,
                               'datetime': datetime_, 'tags': tags, 'src': src})

        return self.items

    def search(self, category: str):
        ''' Search for news given a category
        ### Parameters
            category : str  - News category e.g. politics.
        Returns: 
            list: of dictionaries with sorted values by datetime.
        '''
        self.news = []
        for src, url in self.urls.items():
            if src in [ 'daily_express', 'channel4', 'sky']: //'bbc' removed
                print(f'...scanning {src} news')
                bbc_news = self._get_feed(url.format(
                    category), src=src, category=category)

                self.news.extend(bbc_news)
            else:
                news_items = self._get_feed(url, src=src)
                print(f'...scanning {src} news')
                valid_news = [
                    k for k in news_items if category.lower() in k['tags']]
                self.news.extend(valid_news)

        df = pd.DataFrame(self.news)
        df.sort_values(
            by='datetime', ascending=False, inplace=True)
        self.dict_news = df.to_dict(orient='records')
        return self.dict_news
