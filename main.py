from nltk import word_tokenize
import re
from nltk import SnowballStemmer
import json
import pandas as pd
import tweepy as tw

with open('package/english_stop_words.txt', 'r') as file:
    stop_words = file.read().replace('\n', '')



consumer_key= '0LM8SAYYowA7HHvWt8RGyubNP'
consumer_secret= 'ElThpdi25eGbm8IyeafsP2OhGqmIQHXAt9CkJQM8Cxr5nylGNv'
access_token= '1285807757472522240-lOab72n40SmgBgd28jFuePz5Ykobkn'
access_token_secret= 'TOBoLFjIFJ8Bge8eWWn8UrbADYZ2yYREfmCgnpmLHGBMo'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def predict(text,clf,vectorizer,preprocess):
    t_text = preprocess(text)
    vect_text = vectorizer.transform([t_text])
    out = clf.predict(vect_text)
    return out[0]

text_clean = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

def preprocess(tweet, stem=False):
    stemmer = SnowballStemmer("english").stem

    text = re.sub(text_clean, ' ', str(tweet).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)

    return " ".join(tokens)

def read_topic(file_json):
    topic = json.dumps(file_json)
    return topic


#This is how you predict positive or negative
#print(predict(y,model,vectorizer,preprocess))

def read_topic(file_json):
    topic = json.dumps(file_json)
    return topic


def generate_prediction(request):
    stemmer = SnowballStemmer("english").stem

    def stem_tokenize(text):
        return [stemmer(i) for i in word_tokenize(text)]

    model = pd.read_pickle('package/TwitterModel.pkl')
    Vectorizer = pd.read_pickle('package/Vectorizer.pkl')

    request_json = request.get_json(silent=True)
    topic = read_topic(request_json)

    tweets_popular = tw.Cursor(api.search,
                               q=topic,
                               lang="en",
                               result_type="popular").items(25)
    total_popular = 0
    for tweet in tweets_popular:
        # print(tweet.text)
        total_popular += predict(tweet.text, model, Vectorizer, preprocess)

    #print("Popular Score: ", total_popular / 25)
    #print("Popular Percentage: ", total_popular)  # 100/400 multiplier converts score into a percentage

    tweets_recent = tw.Cursor(api.search,
                              q=topic,
                              lang="en",
                              result_type="recent").items(50)
    total_recent = 0
    for tweet in tweets_recent:
        # print(tweet.text)
        total_recent += predict(tweet.text, model, Vectorizer, preprocess)

    #print("Recent Score: ", total_recent / 50)
    #print("Recent Percentage: ", total_recent / 2)  # Converts Score to a Percentage

    return( json.dumps(round(total_recent/3 + total_popular/3,2) ))


# key = "Kanye"
# tweets_popular = tw.Cursor(api.search,
#                        q=key,
#                        lang="en",
#                        result_type = "popular").items(25)
# total_popular = 0
# for tweet in tweets_popular:
#     #print(tweet.text)
#     total_popular += predict(tweet.text,model,Vectorizer,preprocess)
#
# print("Popular Score: ", total_popular/25)
# print("Popular Percentage: ",total_popular)
#
# tweets_recent = tw.Cursor(api.search,
#                        q=key,
#                        lang="en",
#                        result_type = "recent").items(50)
# total_recent = 0
# for tweet in tweets_recent:
#     #print(tweet.text)
#     total_recent += predict(tweet.text,model,Vectorizer,preprocess)
#
# print("Recent Score: ", total_recent/50)
# print("Recent Percentage: ",total_recent/2) #Converts Score to a Percentage
#
# print(round(total_recent/3 + total_popular/3,2))


