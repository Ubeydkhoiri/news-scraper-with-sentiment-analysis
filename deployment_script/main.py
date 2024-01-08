from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import detik
import cnn
import kompas
import liputan6
import jawapos

import pandas as pd
from pathlib import Path

import concurrent.futures
from functools import partial

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-cookies")

driver = webdriver.Firefox(options=options)

CUR_DIR = Path(__file__).resolve().parent

def main():
    try:
        df_exist = pd.read_csv(f'{CUR_DIR}/data/data.csv')
    except FileNotFoundError:
        print(f"File not found: {CUR_DIR}/data/data.csv")
        df_exist = pd.DataFrame([])

    try:
        date = df_exist['date'].max()
    except KeyError:
        date = "2024-01-01"

    print(date)
    keywords = ['anies baswedan','prabowo subianto','ganjar pranowo']
    data = []
    for keyword in keywords:
        # Create partial functions with fixed parameters
        detik_func = partial(detik.detik_news, keyword=keyword, start_date=date)
        cnn_func = partial(cnn.cnn_news, keyword=keyword, start_date=date)
        kompas_func = partial(kompas.kompas_news, keyword=keyword, start_date=date)
        liputan6_func = partial(liputan6.liputan6_news, keyword=keyword, start_date=date)
        jawapos_func = partial(jawapos.jawapos_news, driver=driver, keyword=keyword, start_date=date)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the tasks
            futures = [ executor.submit(detik_func),
                        executor.submit(cnn_func),
                        executor.submit(kompas_func),
                        executor.submit(liputan6_func),
                        executor.submit(jawapos_func)]

            # Collect the results as they become available
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        for result in results:
            data += result

    driver.close()

    df_result = pd.DataFrame(data)

    df = pd.concat([df_exist, df_result])
    df = df.drop_duplicates()

    return df.to_csv(f'{CUR_DIR}/data/data.csv', index=False)

if __name__=="__main__":
    main()

