#!/usr/bin/python
'''
Author: Megan Ruthven
Date: August 18, 2015
How to use the MegBot summary example:
python megbotex.py [facebook email] [facebook password] [messageID]
'''

import sys 
import json
import re
import string
from collections import Counter
from nltk.corpus import stopwords
from stemming.porter2 import stem
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

import requests 
from splinter import Browser
import urllib2
from bs4 import BeautifulSoup
from megbot import MegBot

maxMessages = 50;
stop = stopwords.words('english')
regex = re.compile('[%s]' % re.escape(string.punctuation))
_intro = "Top words: ";
_megbot_call = "@megbot";
_at_key = "@";
pattern = re.compile("\\b("+_intro+"|"+_megbot_call+")\\W", re.I)

try:
    username = sys.argv[1]
    password = sys.argv[2]
    message  = sys.argv[3]
	
	# with open('userdata.json') as user_data:
	#     username = user_data['username']
	#     password = user_data['password']
	# message = sys.argv[1] or ''
	
    data = json.load(open('config.json'))
    # print data
    stop = stop + [word.lower().strip() for word in data['addedStops']];
    myset = set(stop);
    stop = list(myset);
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    mb = MegBot(username,password);

except IndexError:
	print "Usage: python megbotex.py <username> <password> <output file>"
	sys.exit()

# print stop

def next_set(pastMessages):
    # Checks to see if there are incoming messages.
	# If there are, returns the new ones.
    newMessage = [];
    end = False;
    mb.refresh_messages();
    if len(pastMessages) != 0:
        print "last line of past messages: " + pastMessages[0];
    while len(newMessage) < maxMessages:
        outM = mb.read_messages();
        print outM;
        t = []
        for out in outM:
            if _intro in out:
                print "found my message";
            elif (len(pastMessages) == 0) or (not
				any(out == s for s in pastMessages[:min(len(pastMessages), 4)])):
                t.append(out);
            else:
                print "was not an original message"
                print "but this was original" + ' '.join(t);
                end = True;
                break;

        newMessage = newMessage+t;
        if end:
            print "returning now";
            return newMessage;
        else:
            mb.next_page();

    return newMessage;

def highest_words(mess):
    # Cleans, filters out punctuation
	# Lowers all words in the string in order to count the frequency of each word.
	# Returns top 5 frequent words
    oneStr = ' '.join(mess).lower();
    inWords = re.sub('[^0-9a-zA-Z]+', ' ', regex.sub('', oneStr)).strip();

    totWords = ' '.join([word for word in inWords.split() if word not in stop]);
    print totWords;
    wordCount = Counter(totWords.split());
    print wordCount;
    toGoOut = ', '.join([letter for letter, count in wordCount.most_common(5)]);
    return toGoOut;
    

#set up environment
mb.login();

url = 'https://mbasic.facebook.com/messages/'
mb.browser.visit(url)
text = urllib2.urlopen(url).read()
soup = BeautifulSoup(text, "html.parser")

print soup.prettify()

#data = soup.findAll('a')
#for d in data:
#	link = d.get('href')
#	name = d.get_text()
#	print name, link


#mb.move_to_message(message);

'''
#reading all of the past messages from the group chat
currCheck =[]; # TODO: Unnecessary?
currCheck = next_set(currCheck);
currCheck = currCheck[:maxMessages-1];
print currCheck;
ou = highest_words(currCheck);
print ou;
mb.send_message(_intro + ou);
newMess = 0;
filteredAts = [];
while True:
    try:
        print "checking";
        # Checking to see if the group message has gotten any more messages from
 	    # before.
        n = next_set(currCheck);
        newMess = newMess + len(n);
        currCheck = n + currCheck;
        print newMess;
        print currCheck;

        # If the max amount of messages or a @megbot call have come in, summarize
    	#   the past maxMessages amount of chat and return the top 5 words.
        if (
		    (newMess > maxMessages)
		    or any(_megbot_call in s for s in currCheck[:len(n)])
	       ):
		    currCheck = currCheck[:maxMessages];
		    ou = highest_words(currCheck);
		    mb.send_message(_intro+ou);
		    newMess = 0;
		    print "found another message";

        # Shout out feature.
		# If anyone says "@"xyz that isn't a megbot call.
		# This shouts out the name following the @ in all capitals
        if any(_at_key in s for s in currCheck[:len(n)]):
            foundShoutOut = ' '.join(currCheck[:len(n)]).split();
            for f in foundShoutOut:
                if f[0] == _at_key and _megbot_call not in f:
                    mb.send_message(f[1:].upper());
        
        time.sleep(20);

    except (URLError, selenium.common.exceptions.StaleElementReferenceException):
	print "reconnecting......"
	# Try to reconnect 
	time.sleep(5)
	try:
		login()
	except:
		continue
'''