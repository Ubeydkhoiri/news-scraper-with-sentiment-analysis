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

# Create function to scrape data and get the polarity score 
def detik_news(start_date="2024-01-01", keyword="pilpres 2024"):
    start_date = pd.Timestamp(start_date)
    keyword_url = keyword.replace(' ','-')
    news = []
    
    # Initialize page number
    x = 1
    
    # Loop for scraping pages until the start_date is reached
    while True:
        # Construct the URL for the current page
        url_detik = f'https://www.detik.com/tag/{keyword_url}/?sortby=time&page={x}'
        print(f'scrape detik {keyword} - page:{x}')
        
        # Make a request to the URL and parse the content
        page = requests.get(url_detik)
        soup = BeautifulSoup(page.content, "html.parser")

        # Find all articles on the page
        articles = soup.find_all('article')
        for i in articles:
            # Extract date, URL, and title from the article
            date = i.find('span','date').text.split(',')[1].replace('Des','Dec')
            date = pd.to_datetime(date)
            url = i.find('a').get('href')
            title = i.find('h2','title').text
            # Calculate sentiment score using textblob_score function
            polarity = textblob_score(title)

            # Break the loop if the start_date is greater than the current article's date
            if start_date > date:
                break

            news.append({
                'keyword':keyword,
                'platform':'detikcom',
                'date':date,
                'url':url,
                'title':title,
                'score':polarity
            })
        # Break the main loop if the start_date is greater than the current article's date
        if (start_date>date) or (x==20):
            break

        x += 1 # Move to the next page
        
    return news

if __name__=="__main__":
    data = detik_news()
    print(data)