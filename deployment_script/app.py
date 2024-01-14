from flask import Flask, render_template, url_for, request
import pandas as pd
import joblib
from pathlib import Path
from main import main

CUR_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

dataframe = pd.read_csv(f'{CUR_DIR}/data/data.csv')
dataframe = dataframe.sort_values(['date'], ascending=False)

@app.route('/')
def home():
    return {
        'message':"Hello, thank you for visiting my repository!",
        'routes':[{
            '/export':"Export all data based on keyword",
            '/updatedata':"To update the data"
        }]
        }

@app.route('/export')
def export():
    args = request.args
    keyword = args.get('keyword', type=str)
    if keyword is None:
        result = dataframe.to_dict(orient='records')
        return result
    
    df = dataframe[dataframe['keyword']==keyword]
    if df.to_dict(orient='records') == []:
        return {
            'keyword': keyword,
            'message':f'Data is empty, {keyword} is not presidential candidate'}

    return df.to_dict(orient='records')

@app.route('/updatedata')
def updatedata():
    main()
    return {'status':'success',
            'message':'Data has been updated!'}

if __name__ == '__main__':
    app.run(debug=True)