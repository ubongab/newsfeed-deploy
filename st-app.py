import streamlit as st
from datetime import datetime, timezone, timedelta
import arrow
import re
from newsfeed import NewsFeed

remov_html_tags = re.compile('<.*?>')


now = datetime.now().astimezone(timezone.utc)
two_days_ago = now-timedelta(2)


news = NewsFeed()

st.set_page_config(layout="wide")
st.header('UK NewsFeed')
cats = {'1': 'uk', '2': 'education', '3': 'politics', '4': 'world', '5': 'education', '6': 'business',
        '7': 'health', '8': 'technology', '9': 'entertainment', '10': 'sport'}
user_selection = st.sidebar.radio(
    'Choose a news category', list(cats.values()))
if user_selection:
    nf = news.search(user_selection)
    for k in nf:

        if k['datetime'] > two_days_ago:
            with st.expander(f" {k['title']} - {arrow.get(k['datetime']).humanize()} ({k['src']})"):
                # st.markdown(k['summary'], unsafe_allow_html=True)
                st.write(k['link'])
                st.markdown(k['summary'], unsafe_allow_html=True)
                # st.text(f"{k['src'].title()} News")
