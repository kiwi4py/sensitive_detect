# -*- coding: utf-8 -*-  
        
import string, urllib2
import urllib
from urllib import FancyURLopener
import re

from bs4 import BeautifulSoup

from companysite.models import Sensitive

class MyOpener(FancyURLopener,object):

   version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def get_opener():
    myopener = MyOpener()
    return myopener


def get_sensitive_commentlists(begin_page, end_page, baseUrl):
    content_dict = {}
    myopener = get_opener()
    for i in range(begin_page, end_page+1):
        wholePage = myopener.open(baseUrl + str(i)).read()
        if 'zmid' in wholePage:
            content = find_content(wholePage)
            print content
            if check_sensitive_words(content):
                word =  check_sensitive_words(content)
                content = content.replace(word,  'M'+word+'M') # use 'M' to mark the sensitive word
                content_dict[i] = content
    return content_dict        

# you may have to change this function according to the html file you want to parse      
def find_content(wholePage):
   soup = BeautifulSoup(wholePage)
   class_zmid = soup(class_='zmid') # define your own class name  
   contents = class_zmid[0]
   contents = contents.get_text()
   return contents


def check_sensitive_words(to_check):
   word_list = Sensitive.objects.all() # here Sensitive is a django model object; 
   for word in word_list:
      word = str(word)
      word = word.decode('utf-8')
      if word in to_check:  
          return word
   return False

if __name__ == "__main__":       
    begin_page = 4287
    end_page = 4288
    baseUrl = '' # define your Url here leaving the end id, something like http://www.xxxx.com/comments/
    content_dict = get_sensitive_commentlists(begin_page, end_page, baseUrl)
    print content_dict

   
# this is the end of the file 
