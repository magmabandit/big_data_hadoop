#!/usr/bin/env python
import sys, re
import os
import random

import requests
import re
import string
stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
# get valence collection
valences_list = requests.get("https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt").content
stopwords = list(set(stopwords_list.decode().splitlines()))
valences = dict(line.split('\t') for line in valences_list.decode().splitlines())


def remove_stopwords(words):
    list_ = re.sub(r"[^a-zA-Z0-9]", " ", words.lower()).split()
    return [itm for itm in list_ if itm not in stopwords]


def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('[\d\n]', ' ', text)
    return ' '.join(remove_stopwords(text))

def calc_valence(text):
    total_valence = 0
    for word in text.split(' '):
        if word in valences:
            # cast number string to int
            total_valence += int(valences[word])
    return total_valence

def valence(text):
    # case for encoded string
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    return calc_valence(clean_text(text))

def main(argv):
    # get name of prez by filename
    input_file_path = os.environ.get('map_input_file', '/dev/null')  # Default to '/dev/null' if not set
    prez = os.path.dirname(input_file_path)
    line = clean_text(sys.stdin.readline())
    try:
        while line:
            for word in line:
                print (prez + "\t" + str(valence(word)))
            line = clean_text(sys.stdin.readline())
    except EOFError as error:
        return None

if __name__ == "__main__":
    main(sys.argv)