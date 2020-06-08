#!/usr/bin/python
#-*- coding: utf-8 -*-

import os, re, requests, math
from math import log
from nltk import word_tokenize
from bs4 import BeautifulSoup
from flask import Flask, flash, request, redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


@app.route('/')
def home(ERROR=None, numbers=0):
    return render_template('home.html', ERROR=ERROR, numbers=numbers)


urlList = []
textList = []
countList = []
time = []
wordList = []
numbers = 0

@app.route('/home/textInput', methods=['POST'])
def request_url():
    global numbers

    if request.method == 'POST':
        try :
            url = request.form['URL']
        except :
            ERROR = "실패 : 부정확한 ULR 주소를 입력하셨습니다."
            return render_template('home.html', ERROR=ERROR)
    
    res = requests.get(url)

    html = BeautifulSoup(res.content, "html.parser")
    
    urlList.append(url)
    textList.append(html.text)
    countList.append(process_new_sentence(html.text))
    time.append(1)
    numbers+=1

    return render_template('home.html', urlList=urlList, countList=countList, time=time, numbers=numbers ) 

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/home/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            ERROR = "실패 : 존재하지 않는 파일입니다."
            return render_template('home.html', ERROR=ERROR)

        f = request.files['file']

        if f.filename == '':
            ERROR = "실패 : 파일을 정하지 않았습니다."
            return render_template('home.html', ERROR=ERROR)

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(filename)
            
            f = open(filename, 'r')
            
            global numbers

            while True:
                url = f.readline().strip()
                
                if not url:
                    break

                if url in urlList:
                    ERROR = " 중복 : 중복된 url을 입력하셨습니다."
                    return render_template('home.html', ERROR=ERROR)

                try :
                    res = requests.get(url)
                except :
                    if res.status_code == 302:
                        ERROR = "실패 : 인터넷에 연결되어 있지 않습니다."
                    else:
                        ERROR = "실패 : 부정확한 주소를 입력하셨습니다."
                    
                    return render_template('home.html', ERROR=ERROR)

                html = BeautifulSoup(res.content, "html.parser")
                        
                urlList.append(url)
                textList.append(html.text)
                countList.append(process_new_sentence(html.text))
                time.append(1)
                numbers += 1
        

    return render_template('home.html', urlList=urlList, countList=countList, time=time, numbers=numbers )

word_d = {}
sent_list = []

def process_new_sentence(s):
        sent_list.append(s)
        tokenized = word_tokenize(s)

        for word in tokenized:
            if word not in word_d.keys():
                word_d[word]=0
            word_d[word] += 1
        
        return len(tokenized)
        

def compute_tf(s):
	bow = set()
	# dictionary for words in the given sentence (document)
	wordcount_d = {}

	tokenized = word_tokenize(s)
	for tok in tokenized:
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok] += 1
		bow.add(tok)
	tf_d = {}
	for word,count in wordcount_d.items():
		tf_d[word]=count/float(len(bow))
	return tf_d



def compute_idf():
	Dval = len(sent_list)
	# build set of words
	bow = set()

	for i in range(0,len(sent_list)):
		tokenized = word_tokenize(sent_list[i])
		for tok in tokenized:
			bow.add(tok)

	idf_d = {}
	for t in bow:
		cnt = 0
		for s in sent_list:
			if t in word_tokenize(s):
				cnt += 1
			
		idf_d[t]=log(Dval/cnt)
	return idf_d


def tf_idf(s, n):
	for i in range(len(s)):
		process_new_sentence(s[i])
	
	idf_d = compute_idf()
	for i in range(0,len(sent_list)):
		tf_d = compute_tf(sent_list[i])
		result ={}

		for word,tfval in tf_d.items():
			result[word]=tfval*idf_d[word]
		result2 = sorted(result.items(), key=lambda x: x[1], reverse=True)

		ret={}
		ret2=[]	
		for j in range(0, 10):
			
			if j>len(result2)-1:
				break;
			#ret[result2[j][0]]=result2[j][1]
			ret2.append(result2[j][0])
			#print(type(result2[j][0]))
		
			
		if n==i:
			return ret2

@app.route('/home/word_analysis', methods=['POST'])
def print_analysis():

    if request.method == 'POST':
        index = request.form['index']
        tf_idfWordList = tf_idf(textList, int(index))
        return render_template('word_analysis.html', parsed_page=tf_idfWordList)

def process_new_sentence_1(s):
	word_d = {}

	tokenized = word_tokenize(s)

	for word in tokenized:
		if word not in word_d.keys():
			word_d[word] = 0
		word_d[word] += 1

	return word_d

def make_vector(word_d,s):
	v = []
	tokenized = word_tokenize(s)

	for w in word_d.keys():
		val = 0
		for t in tokenized:
			if t == w:
				val += 1
		v.append(val)
	return v

def cos(s, n):
	url_d = {}
#urlList의 원소를 key값으로, v리스트를 value로 하는 딕셔너리
#url_d = { 'www.aaa' : [1, 1, 0, 1], 'www.bbb': [1, 0, 1, 1]}
	for i in range(len(s)):
		word_d = process_new_sentence_1(s[i])
		v_list = make_vector(word_d, s[i])
		url_d[urlList[i]] = v_list

	v1 = url_d[urlList[n]] 
	url_cossi = {} 
	for i in range(len(s)):
		if i==n:
			continue 
		v2 = url_d[urlList[i]] #v1과 비교할 v리스트들 
		dotpro = numpy.dot(v1,v2)
		cossimil = dotpro / (norm(v1)*norm(v2))
		url_cossi[urlList[i]] = cossimil
	
	url_cossi = sorted(url_cossi.items(), key=lambda x:x[1], reverse = True)
	top_url = []
	for i in range(3):
		top_url.append(url_cossi[i][0])
	
	return top_url
		
@app.route('/home/cos_simil', methods=['POST'])

def print_top_simil():
	if request.method == 'POST':
		index = request.form['index']
	top_url = cos(textList, int(index))
		
	return render_template('cos_simil.html', top_url=top_url)
		

if __name__ == '__main__':
    app.run(debug = True)
