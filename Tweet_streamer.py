from tweepy import Stream
import tweepy
from tweepy.streaming import StreamListener
import psycopg2
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

conn = psycopg2.connect(
    host="localhost",
    database="tweets",
    user="jarvis",
    password="tests@654",
)

def create_table():
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
    conn.commit()
    cur.close()

create_table()


ckey= "W5wD6xJKFTLry8c4XbKb3K7TN"
csecret= "LDSsat8kWGaPG3HdavumusZyf60F8QrbLbdg2SxpMvBiG4pSTq"
atoken = "1388914208616505346-jE7MWIxJte3XFHkqt6Ux8kodYcd4tI"
asecret= "M99lBNNXCEwzox7ROBoarLDd2lbEc069fXyzKGGDBAW7h"

class Listener(StreamListener):
    def on_data(self,data):
        try:
            cur = conn.cursor()
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            
            insert_sql = ("INSERT INTO sentiment (unix, tweet, sentiment)" "VALUES (%s, %s, %s)")
            data = (time_ms, tweet, sentiment)
            
            cur.execute(insert_sql,data)
            conn.commit()
        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)

while True:
    try:
        auth = tweepy.OAuthHandler(ckey,csecret)
        auth.set_access_token(atoken,asecret)

        # api = tweepy.API(auth)
        # pt = api.home_timeline()
        # print(pt)

        twitterStream = Stream(auth,Listener())
        twitterStream.filter(track=["Nifty 50"])
    except Exception as e:
        print(str(e))
        time.sleep(5)
            