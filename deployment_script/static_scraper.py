import requests 
from bs4 import BeautifulSoup  
import pandas as pd
from blob import textblob_score

import warnings
warnings.filterwarnings('ignore')


parser = "html.parser"
default_keyword = "pipres 2024"

# Create function to scrape data and get the polarity score 
def detik_news(start_date="2024-01-01", keyword=default_keyword):
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
        soup = BeautifulSoup(page.content, parser)

        # Find all articles on the page
        articles = soup.find_all('article')
        for i in articles:
            try:
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
            except Exception as e:
                print('error message detik:', e)

        # Break the main loop if the start_date is greater than the current article's date
        if (start_date>date) or (x==20):
            break

        x += 1 # Move to the next page
        
    return news

### CNN
def cnn_news(start_date="2024-01-01", keyword=default_keyword):
    start_date = pd.Timestamp(start_date)
    keyword_url = keyword.replace(' ','-')
    news = []
    
    x = 1

    while True:
        url_cnn = f'https://www.cnnindonesia.com/tag/{keyword_url}/{x}'
        print(f'scrape cnn {keyword} - page:{x}')
        
        page = requests.get(url_cnn)
        soup = BeautifulSoup(page.content, parser)

        articles = soup.find_all('article')
        for i in articles:
            try:
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
            except Exception as e:
                print('error message cnn:', e)
            
        if (start_date>date) or (x==20):
            break

        x += 1
        
    return news

## KOMPAS
def kompas_news(start_date="2024-01-01", keyword=default_keyword):
    start_date = pd.Timestamp(start_date)
    keyword_url = keyword.replace(' ','-')
    news = []
    
    x = 1
    
    while True:
        url_kompas = f'https://www.kompas.com/tag/{keyword_url}?page={x}'
        print(f'scrape kompas {keyword} - page:{x}')
        
        page = requests.get(url_kompas)
        soup = BeautifulSoup(page.content, parser)

        articles = soup.find_all('div','article__list clearfix')
        for i in articles:
            try:
                title = i.find('a', 'article__link').text
                url = i.find('a', 'article__link').get('href')
                date = i.find('div','article__date').text.replace('Des','Dec')
                date = pd.to_datetime(date, dayfirst=True)
                polarity = textblob_score(title)

                if start_date>date:
                    break

                news.append({
                    'keyword':keyword,
                    'platform':'kompas',
                    'date':date,
                    'url':url,
                    'title':title,
                    'score':polarity
                })
            except Exception as e:
                print('error message kompas:', e)
            
        if (start_date>date) or (x==20):
            break

        x += 1 
        
    return news

## LIPUTAN6
def liputan6_news(start_date="2024-01-01", keyword=default_keyword):
    start_date = pd.Timestamp(start_date)
    keyword_url = keyword.replace(' ','-')
    news = []
    
    x = 1
    
    while True:
        url_liputan6 = f'https://www.liputan6.com/tag/{keyword_url}?page={x}'
        print(f'scrape liputan6 {keyword} - page:{x}')
        
        page = requests.get(url_liputan6)
        soup = BeautifulSoup(page.content, parser)

        articles = soup.find_all('header','articles--iridescent-list--text-item__header')
        for i in articles:
            try:
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
            except Exception as e:
                print('error message liputan6:', e)
            
        if (start_date>date) or (x==20):
            break

        x += 1 
        
    return news

if __name__=="__main__":
    data = detik_news()
    print(data)