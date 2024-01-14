# News Scraper Tutorial

## Overview
Welcome to the News Scraper tutorial repository! This repository serves as a comprehensive guide for web scraping using BeautifulSoup and Selenium. In this tutorial, you will learn how to scrape news from websites like detik[dot]com. 

Additionally, we'll focus on scraping news related to Indonesia's presidential candidates for 2024, using keywords such as **"anies baswedan"**, **"prabowo subianto"**, and **"ganjar pranowo"**.

## Repository Structure
- **img/** 
- **img_save/** 
- **notebook/**
  - `static_web.ipynb`: Jupyter notebook for scraping news from traditional static websites.
  - `dynamic_web.ipynb`: Jupyter notebook for scraping news from dynamic web applications.
- **deployment_script/:** Contains scripts and files for deployment using Flask. 
- `requirements.txt`

## Tutorial Contents
- **Static Web Scraping Tutorial**: Explore the notebook/static_web.ipynb notebook to learn how to scrape news from traditional static websites.

- **Dynamic Web Scraping Tutorial**: The notebook/dynamic_web.ipynb notebook guides you through scraping news from dynamic web applications.

Sentiment Analysis Tutorial: Learn lexicon-based sentiment analysis using TextBlob. Understand the sentiment behind news articles related to the selected keywords. Build a machine learning model from scratch for sentiment analysis. 

## Getting Started
1. **Clone the repository to your local machine**
    ```bash
    git clone https://github.com/Ubeydkhoiri/news-scraper.git
    ```
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Navigate to the repository**
    ```bash
    cd news-scraper
    ```
4. **Run flask app.py**
    ```bash
    python deployment_script/app.py
    ```
    After flask app runs, you can copy http://127.0.0.1:5000 on your web-browser. Edit your route http://127.0.0.1:5000/export?keyword='anies baswedan' to export all news with tag 'anies baswedan'. And http://127.0.0.1:5000/updatedata to run the scraper and update the data

5. Explore the tutorials in the notebook directory and deploy the Flask application using the scripts in deployment_script.

#### Note: Stay tuned for more tutorials as the project progresses!