from textblob import TextBlob

def textblob_score(text):
    """
    The `text_en.sentiment` method provides two values: polarity and subjectivity.
    - Polarity ranges from -1.0 to 1.0, indicating the sentiment's negativity to positivity.
    - Subjectivity ranges from 0.0 to 1.0, where 0.0 is very factual, and 1.0 is very opinion-based.
    In our case, we focus on the polarity score to understand the sentiment's direction.
    """
    blob_object = TextBlob(text) # get texblob object
    try:
        text_en = blob_object.translate(from_lang='id', to='en') # translate into english
    except Exception:
        text_en = blob_object
    score = text_en.sentiment.polarity # extract polarity score
    return score

if __name__=="__main__":
    teks = "My name is ubeyd"
    print(textblob_score(teks))