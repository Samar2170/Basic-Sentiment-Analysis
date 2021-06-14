from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
analyzer = SentimentIntensityAnalyzer()

pos_count = 0
neg_count = 0
pos_correct = 0
neg_correct = 0

df = pd.read_csv('Data/Movie_Reviews/IMDB Dataset.csv')
df = df[:1000]

for i,r in df.iterrows():
    if r['sentiment']== "positive":
        pos_count+=1
    else:
        neg_count+=1    



for i,r in df.iterrows():
    line = r['review']
    vs = analyzer.polarity_scores(line)
    if not vs['neg'] > 0.1:
        if vs['pos']-vs['neg'] >0 and r['sentiment'] == 'positive':
            pos_correct+=1
    elif not vs['pos'] > 0.1:
        if vs['pos']-vs['neg'] <=0 and r['sentiment'] =='negative':
            neg_correct+=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))


    # if vs['compound'] >0  and r['sentiment'] == "positive":
    #     pos_correct+=1
    # elif vs['compound'] <0  and r['sentiment'] == "negative":
    #     neg_correct+=1   
    
