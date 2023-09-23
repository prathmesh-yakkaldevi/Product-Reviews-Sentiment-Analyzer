import re
import os
import nltk
import joblib
import requests
import numpy as np
from bs4 import BeautifulSoup
import urllib.request as urllib
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud,STOPWORDS
from flask import Flask,render_template,request
import time

os.environ['NLTK_DATA'] = os.getcwd()
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# word_2_int = joblib.load('word2int.sav')
# model = joblib.load('sentiment.sav')
# stop_words = set(open('stopwords.txt'))

def clean(x):
    x = re.sub(r'[^a-zA-Z ]', ' ', x) # replace evrything thats not an alphabet with a space
    x = re.sub(r'\s+', ' ', x) #replace multiple spaces with one space
    x = re.sub(r'READ MORE', '', x) # remove READ MORE
    x = x.lower()
    x = x.split()
    y = []
    for i in x:
        if len(i) >= 3:
            if i == 'osm':
                y.append('awesome')
            elif i == 'nyc':
                y.append('nice')
            elif i == 'thanku':
                y.append('thanks')
            elif i == 'superb':
                y.append('super')
            else:
                y.append(i)
    return ' '.join(y)


def extract_all_reviews(url, clean_reviews, org_reviews,customernames,commentheads,ratings):
    with urllib.urlopen(url) as u:
        page = u.read()
        page_html = BeautifulSoup(page, "html.parser")
    reviews = page_html.find_all('div', {'class': 't-ZTKy'})
    commentheads_ = page_html.find_all('p',{'class':'_2-N8zT'})
    customernames_ = page_html.find_all('p',{'class':'_2sc7ZR _2V5EHH'})
    ratings_ = page_html.find_all('div',{'class':['_3LWZlK _1BLPMq','_3LWZlK _32lA32 _1BLPMq','_3LWZlK _1rdVr6 _1BLPMq']})

    for review in reviews:
        x = review.get_text()
        org_reviews.append(re.sub(r'READ MORE', '', x))
        clean_reviews.append(clean(x))
    
    for cn in customernames_:
        customernames.append('~'+cn.get_text())
    
    for ch in commentheads_:
        commentheads.append(ch.get_text())
    
    ra = []
    for r in ratings_:
        try:
            if int(r.get_text()) in [1,2,3,4,5]:
                ra.append(int(r.get_text()))
            else:
                ra.append(0)
        except:
            ra.append(r.get_text())
        
    ratings += ra
    # print(ratings)

def tokenizer(s):
    s = s.lower()      # convert the string to lower case
    tokens = nltk.tokenize.word_tokenize(s) # make tokens ['dogs', 'the', 'plural', 'for', 'dog']
    tokens = [t for t in tokens if len(t) > 2] # remove words having length less than 2
    tokens = [t for t in tokens if t not in stop_words] # remove stop words like is,and,this,that etc.
    return tokens

def tokens_2_vectors(token):
    X = np.zeros(len(word_2_int)+1)
    for t in token:
        if t in word_2_int:
            index = word_2_int[t]
        else:
            index = 0
        X[index] += 1
    X = X/X.sum()
    return X


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results',methods=['GET'])
def result():    
    url = request.args.get('url')
    nreviews = int(request.args.get('num'))
    clean_reviews = []
    org_reviews = []
    customernames = []
    commentheads = []
    ratings = []

    with urllib.urlopen(url) as u:
        page = u.read()
        page_html = BeautifulSoup(page, "html.parser")
    
    proname = ""
    proname = page_html.find('div', class_='_2s4DIt _1CDdy2').text
    soup = page_html
    price = "Could not get"
    price = soup.find('div', class_='_30jeq3').text
    review_div = soup.find_all('div', class_='t-ZTKy')
    review_stars = soup.find_all('div', class_='_3LWZlK _1BLPMq')
    review_name = soup.find_all('p', class_='_2sc7ZR _2V5EHH')
    review_head = soup.find_all('p', class_='_2-N8zT')
    d = []
    for i in range(len(review_div)):
        if(i == nreviews):
            break
        x = {}
        x['review'] = review_div[i].text
        # x['sent'] = predictions[i]
        x['cn'] = review_name[i].text
        x['ch'] = review_head[i].text
        # print( x['review'], "----*---")
        x['stars'] = int(review_stars[i].text)
        if(x['stars'] >= 3):
            x['sent'] = 'POSITIVE'
        else:
            x['sent'] = 'NEGATIVE'
        d.append(x)

    review = []
    for x in review_div:
        review.append(x.text)
    for_wc = ' '.join(review)
    wcstops = set(STOPWORDS)
    wc = WordCloud(width=1400,height=800,stopwords=wcstops,background_color='white').generate(for_wc)
    plt.figure(figsize=(20,10), facecolor='k', edgecolor='k')
    plt.imshow(wc, interpolation='bicubic') 
    plt.axis('off')
    plt.tight_layout()
    CleanCache(directory='static/images')
    plt.savefig('static/images/woc.png')
    plt.close()

    review_stars_list = []
    for x in review_stars:
        review_stars_list.append(int(x.text))
    ratings = [1, 2, 3, 4, 5]
    quantity = [0,0,0,0,10]
    for x in review_stars_list:
    # print(x)
        quantity[x-1] = quantity[x-1]+1
    # print(quantity)
    # quantity = [500, 100, 249, 100, 50]
    plt.figure(figsize=(5, 5))
    plt.pie(quantity, labels=ratings, autopct='%1.1f%%', startangle=0, pctdistance=0.85)
    plt.axis('equal')
    plt.title("Sample Ratings Distribution")
    # plt.show()
    plt.savefig('static/images/pie.png')
    plt.close()
    # url = url_for('static', filename='images/pie.png')


    np,nn =0,0
    for i in d:
        if i['sent']=='NEGATIVE':nn+=1
        else:np+=1
    # print(d)
    return render_template('result.html',dic=d,n=nreviews,nn=nn,np=np,proname=proname,price=price)

    
@app.route('/wc')
def wc():
    return render_template('wc.html')


class CleanCache:
	'''
	this class is responsible to clear any residual csv and image files
	present due to the past searches made.
	'''
	def __init__(self, directory=None):
		self.clean_path = directory
		# only proceed if directory is not empty
		if os.listdir(self.clean_path) != list():
			# iterate over the files and remove each file
			files = os.listdir(self.clean_path)
			for fileName in files:
				# print(fileName)
				os.remove(os.path.join(self.clean_path,fileName))
		print("cleaned!")


if __name__ == '__main__':
    app.run(debug=True)
