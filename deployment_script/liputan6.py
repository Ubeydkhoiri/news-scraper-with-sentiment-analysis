import requests 
from bs4 import BeautifulSoup  
import pandas as pd
from textblob import TextBlob

import warnings
warnings.filterwarnings('ignore')


def textblob_score(text):
    """
    The `text_en.sentiment` method provides two values: polarity and subjectivity.
    - Polarity ranges from -1.0 to 1.0, indicating the sentiment's negativity to positivity.
    - Subjectivity ranges from 0.0 to 1.0, where 0.0 is very factual, and 1.0 is very opinion-based.
    In our case, we focus on the polarity score to understand the sentiment's direction.
    """
    blob_object = TextBlob(text) # get texblob object
    text_en = blob_object.translate(from_lang='id', to='en') # translate into english
    score = text_en.sentiment.polarity # extract polarity score
    return score

def liputan6_news(start_date="2024-01-01", keyword="pilpres 2024"):
    start_date = pd.Timestamp(start_date)
    keyword_url = keyword.replace(' ','-')
    news = []
    
    x = 1
    
    while True:
        url_liputan6 = f'https://www.liputan6.com/tag/{keyword_url}?page={x}'
        print(f'scrape liputan6 {keyword} - page:{x}')
        
        page = requests.get(url_liputan6)
        soup = BeautifulSoup(page.content, "html.parser")

        articles = soup.find_all('header','articles--iridescent-list--text-item__header')
        for i in articles:
            date = i.find('time','articles--iridescent-list--text-item__time timeago').text.replace('Des','Dec')
            date = pd.to_datetime(date)
            title = i.find('a','ui--a articles--iridescent-list--text-item__title-link').get('title')
            url = i.find('a','ui--a articles--iridescent-list--text-item__title-link').get('href')
            polarity = textblob_score(title)

            if start_date>date:
                break

            news.append({
                'keyword':keyword,
                'platform':'liputan6',
                'date':date,
                'url':url,
                'title':title,
                'score':polarity
            })
            
        if (start_date>date) or (x==20):
            break

        x += 1 
        
    return news

if __name__=="__main__":
    data = liputan6_news()
    print(data)