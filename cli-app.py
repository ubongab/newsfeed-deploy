import typer
import arrow
from enum import Enum
from newsfeed import NewsFeed

app = typer.Typer()
n = NewsFeed()


class Category(Enum):
    education = 'education'
    sport = 'sport'
    uk = 'uk'
    politics = 'politics'
    entertainment = 'entertainment'
    business = 'business'
    health = 'health'
    science = 'science'
    technology = 'technology'


@app.command()
def news(cat: Category, total: int = typer.Argument(10)):
    '''Display news items'''
    print(f'{cat.value} News')
    for item in n.search(cat.value)[:total]:
        print('-----------------------------------------------------------------------------------------------------')
        print(item['title'])
        print(item['link'])
        print(
            f"{arrow.get(item['datetime']).humanize()} \tsource: {item['src']}")
    print('-----------------------------------------------------------------------------------------------------\n')


if __name__ == '__main__':
    app()
