# Import libraries
import pandas as pd
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.by import By

# Filter out warning messages to improve code readability
import warnings
warnings.filterwarnings('ignore')  # Ignore warning messages

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

def jawapos_news(driver, keyword, start_date):
    keyword_url = keyword.replace(' ','-')
    start_date = pd.Timestamp(start_date)
    
    month_map = {'Desember':'Dec', 'Januari':'Jan'}
    news = []    
    x = 1
    while True:
        url_jawa = f'https://www.jawapos.com/tag/{keyword_url}?page={x}'
        print(f'scrape jawapos {keyword} - page:{x}')
        
        driver.get(url_jawa)

        articles = driver.find_elements(By.CLASS_NAME, 'latest__item')
        for i in articles:
            url = i.find_element(By.CLASS_NAME, 'latest__link').get_attribute('href')
            title = i.find_element(By.CLASS_NAME, 'latest__link').text
            date = i.find_element(By.CLASS_NAME, 'latest__date').text
            
            # Process and standardize the date format
            date = date.split(',')[1].replace('|','')
            for i,j in month_map.items():
                date = date.replace(i,j)
            date = pd.to_datetime(date)
            polarity = textblob_score(title)
            
            # If the article date is earlier than the specified start_date, stop collecting
            if start_date > date:
                break

            # Append the news information to the 'news' list
            news.append({
                'keyword': keyword,
                'platform': 'jawapos',
                'date': date,
                'url': url,
                'title': title,
                'score':polarity
            })
            
        # Check if start_date is reached or if the maximum page limit (20) is reached
        if (start_date > date) or (x == 20):
            break
            
        # Move to the next page
        x += 1
    
    # Return the collected news information
    return news

if __name__=='__main__':
    # Create a new Firefox WebDriver instance
    driver = webdriver.Firefox()
    data = jawapos_news(driver=driver, keyword='anies baswedan', start_date='2024-01-01')
    print(data)
    driver.close()