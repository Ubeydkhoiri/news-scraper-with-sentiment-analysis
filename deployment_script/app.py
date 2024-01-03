from flask import Flask, render_template, url_for, request
import pandas as pd
import joblib
from pathlib import Path

CUR_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

data = joblib.load(f'{CUR_DIR}/data/data.joblib')
dataframe = pd.DataFrame(data)

@app.route('/')
def home():
    return "Hello World"

@app.route('/scrape')
def scrape():
    args = request.args
    keyword = args.get('keyword', default='', type=str)
    df = dataframe[dataframe['keyword']==keyword]
    result = df.to_dict(orient='records')

    return result

if __name__ == '__main__':
    app.run(debug=True)