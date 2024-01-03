import detik
import joblib
from pathlib import Path

CUR_DIR = Path(__file__).resolve().parent

def main():
    keywords = ['anies baswedan','prabowo subianto','ganjar pranowo']
    data = [] 
    for keyword in keywords:
        result = detik.scrape_news(keyword=keyword)
        data += result

    return joblib.dump(data, f'{CUR_DIR}/data/data.joblib')

if __name__=="__main__":
    main()

