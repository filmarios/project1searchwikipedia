# import the XML file named "wiki.xml"

import xml.etree.ElementTree as etree
import csv
import re


# the import procedure is heavily inspired by http://www.heatonresearch.com/2017/03/03/python-basic-wikipedia-parsing.html 
# and https://www.ibm.com/developerworks/library/x-hiperfparse/index.html.

def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

# open the article.csv that we are going to append to.
with open('articles.csv', "w", encoding='utf-8') as articles:
    articlesWriter = csv.writer(articles, quoting=csv.QUOTE_MINIMAL)
    # use etree, and look for events start and end.
    for event, elem in etree.iterparse('wiki.xml', events=('start', 'end')):
        
        tname = strip_tag_name(elem.tag)
        
        # upon start of a page tag
        if event == 'start':
            if tname == 'page':
                title = ''
                text = ''
        # By the end of each pages tag, app
        else:
            if tname == 'title':
                try:
                    title = elem.text.lower().strip()
                except:
                    title = title
                    
            elif tname == 'text':
                try:
                    text = elem.text
                # if the text is of None type, discard it in the following step
                except:
                    text = "#REDIRECT"
                    
            elif tname == 'ns':
                ns = int(elem.text)
                if (ns == 0):
                    article = True
                else:
                    article = False
                    
            elif tname == 'page':                                
                # sometimes the elem.text is of type None, therefore try is used.
                try:
                    # check whether the article is in fact an article, ns = 0, and does not begin with redicret.
                    if '#REDIRECT' not in text[0:20] and article == True:
                        # remove all newlines and make the string lowercase
                        text = re.sub('\s+',' ',text).lower().strip()
                        # append to csv file
                        articlesWriter.writerow([title, text])
                except TypeError:
                        text = text     
            # clear element to save memory.
            elem. clear()
