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

def cnn_news(start_date="2024-01-01", keyword="pilpres 2024"):
    start_date = pd.Timestamp(start_date)
    keyword_url = keyword.replace(' ','-')
    news = []
    
    x = 1

    while True:
        url_cnn = f'https://www.cnnindonesia.com/tag/{keyword_url}/{x}'
        print(f'scrape page:{x}')
        
        page = requests.get(url_cnn)
        soup = BeautifulSoup(page.content, "html.parser")

        articles = soup.find_all('article')
        for i in articles:
            title = i.find('h2').text
            url = i.find('a').get('href')
            date = url.split('/')[4].split('-')[0]
            date = pd.to_datetime(date)
            polarity = textblob_score(title)

            if start_date>date:
                break

            news.append({
                'keyword':keyword,
                'platform':'cnn',
                'date':date,
                'url':url,
                'title':title,
                'score':polarity
            })
            
        if (start_date>date) or (x==25):
            break

        x += 1
        
    return news

if __name__=="__main__":
    data = cnn_news()
    print(data)