from flask import Flask, render_template
from datetime import datetime, timezone, timedelta
from newsfeed import NewsFeed
from top_stories import TopStories
import arrow
import re


app = Flask(__name__)

news = NewsFeed()
t = TopStories()
top = t.top

now = datetime.now().astimezone(timezone.utc)
two_days_ago = now-timedelta(2)
remove_tags = re.compile("<.*?>")


def page_manager(category):
    news_list = news.search(category)
    news_items = [
        item for item in news_list if item['datetime'] > two_days_ago]
    for item in news_items:
        item['date_str'] = arrow.get(item['datetime']).humanize()
        item['summary'] = re.sub(remove_tags, ' ', item['summary'])
    return news_items[:15]


@app.route("/")
@app.route("/<category>/")
def page(category='uk'):
    current_news = page_manager(category)
    return render_template('index.html', current_news=current_news,
                           year=datetime.now().year, category=category, top=top)


if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0', port=5000)
