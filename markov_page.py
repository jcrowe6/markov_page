from bs4 import BeautifulSoup
import requests
import numpy as np
import sys
import random
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def helloworld():
    return "<marquee><h1>Hello world!!</h1></marquee>"

def get_pages_lines(url):
    response = requests.get(url)
    print(__name__ + ": Got webpage!")
    soup = BeautifulSoup(response.text, features='html.parser')
    lines = soup.get_text().lower().split('\n')
    lines = list(filter(lambda e : len(e) > 20 , lines))
    lines = list(map(lambda e : e.split(), lines))
    # lines is now a list of lists of strings 
    return lines

def create_sent_from_lines(lines):
    words_dict = {} # dict, key: a word, value: dict of next words and their occurrances
    # ex. words_dict["the"] == {"dog" : 2, "man" : 3}
    for line in lines:
        for i in range(len(line) - 1):
            word = line[i]
            nextword = line[i+1]
            if word not in words_dict:
                words_dict[word] = {}
            if nextword not in words_dict:
                words_dict[nextword] = {}
            
            if nextword in words_dict[word]:
                words_dict[word][nextword] += 1
            else:
                words_dict[word][nextword] = 1

    sentence = ""
    length = 0
    currword = sys.argv[1]
    while length < 30:
        sentence += currword + " "
        length += 1
        options = []
        total = 0
        for word in words_dict[currword]:
            for i in range(words_dict[currword][word]):
                options.append(word)
                total += 1
        if (len(options) == 0):
            break
        r = random.randint(0, total-1)
        currword = options[r]


    #print("    " + sentence)
    return sentence
    