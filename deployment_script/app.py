from flask import Flask, render_template, url_for, request
import joblib
from IPython.display import HTML

app = Flask(__name__)

df = joblib.load('data.joblib')

@app.route('/')
def home():
    return "Hello World"

@app.route('/scrape')
def scrape():
    args = request.args
    query = args.get('query', default='', type=str)
    start_date = args.get('startDate', default='2024-01-01', type=str)
    
    return render_template(HTML(df.to_html(classes='table table-stripped')))

if __name__ == '__main__':
    app.run(debug=True)