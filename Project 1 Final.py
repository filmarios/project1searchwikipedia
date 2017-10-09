
# coding: utf-8

# In[111]:

# import the XML file named "wiki.xml"

import xml.etree.ElementTree as etree
import csv
import re

def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

with open('articles.csv', "w", encoding='utf-8') as articles:
    articlesWriter = csv.writer(articles, quoting=csv.QUOTE_MINIMAL)
    # make headers in the csv.
    articlesWriter.writerow(['title', 'article'])
    for event, elem in etree.iterparse('wiki.xml', events=('start', 'end')):
        tname = strip_tag_name(elem.tag)
        
        if event == 'start':
            if tname == 'page':
                title = ''
                text = ''
                
        # By the end of each tag, app
        else:
            if tname == 'title':
                try:
                    title = elem.text.lower().strip()
                except:
                    title = title
                    
            elif tname == 'text':
                try:
                    text = elem.text
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
                    if '#REDIRECT' not in text[0:20] and article == True:
                        # remove all newlines and make the string lowercase
                        text = re.sub('\s+',' ',text).lower().strip()
                        articlesWriter.writerow([title, text])
                except TypeError:
                        text = text                
            elem. clear()


import re
from datetime import datetime

# transform the parse string to something useful.
def parse_query(query):
    query = query.replace("'", '').replace('(', '').replace(')', '').split( )
    words = query[::2]
    indexes = [[int(index.split(',')[0]),int(index.split(',')[1])] for index in query[1::2]]
    word_length = [len(word) for word in words]
    return words, indexes, word_length

# check if there are in fact any of the words in the article.
def all_strings_exist(words,article):
    if (len([True for word in words if word in article])==len(words)):
        return True
    else:
        return False

# generate a list of matches for each word in the given article.
def index_of_words(word_length,words,article):
    matches = []
    # use regex to identify the indexes of the words.
    for word in words:
        # construct the matches_count list of lists.
        matches.append([word.start() for word in re.finditer(word,article)])
    return matches

# generate a list for each string with the matching properties of the following string.
def matches_count(indexes,word_length,words,matches):
    matches_count = matches
    # iterate the matches list rows
    for row in range(len(words)-1):
        # iterate the matches list columns
        for col in range(len(matches[row])):
            # create a range to see if it is part of it.
            newRange = range(indexes[row][0]+matches[row][col]+word_length[row],
                             indexes[row][1]+matches[row][col]+word_length[row])
            # Check for each entry of the nex row, if there is a match between that word and the range.
            matches_count[row][col] = [1 if x in newRange else 0 for x in matches[row+1]]
    return matches_count

# generate a list of matches for each string
def matching_string_indexes(words,matches_count,matches):
    fin_match = []
    for col in range(len(matches_count[0])):
        layer = 0
        s_list = matches[layer][col]
        index = [ind for ind, value in enumerate(s_list) if value == 1]
        for layer in range(1,len(words)):
            match_lists = [matches[layer][i] for i in index]
            index = []
            if (layer < len(words)-1):
                for match in match_lists:
                    ind = [ind for ind, value in enumerate(match) if value == 1]
                    index = index + ind
            else:
                fin_match.append(match_lists)
    return fin_match

##### for the whole csv ######

#query = "'cat' (2,5) 'hat' (1,20) 'home'"
#article = "i have a really nice cat cat cat in hat hat at home. my home is lovely"

def check_wiki(article,query):
    
    words, indexes, word_length = parse_query(query)
    # if the strings are all present in the article.
    
    if (all_strings_exist(words,article)==True):
        
        mtch = index_of_words(word_length,words,article)
        mtch_cnt = matches_count(indexes,word_length,words,mtch)
        fin_match = matching_string_indexes(words,mtch_cnt,mtch)
        
        index_start = [word.start() for word in re.finditer(words[0],article)]
        #print indexes
        match_indexes=[]
        #print len(mtch[0])
        #print len(word_length)
        #print len(index_start)
        #print len(fin_match)
        #print fin_match[25][0]
        for i in range(len(index_start)):
            if (sum(fin_match[i])!=0):
                for n in range(len(fin_match[i])):
                    match_indexes.append((index_start[i],fin_match[i][n]+word_length[-1]))
        return match_indexes
    else:
        return False

    

# query = "'cat' (0,10) 'are' (0,10) 'to'"
# query = "'cat' (0,100) 'anatomy'"
# query = "'china' (30,150) 'washington'"
# query =  "'english' (0,200) 'cat'"

query =  "'kitten' (15,85) 'cat' (0,100) 'sire' (0,200) 'oxford'"

startTime = datetime.now()
matches = check_wiki(article,query)

finishingTime = datetime.now() - startTime
print "Time: "
print finishingTime
cnt=0
for index in matches:
    print index 
    print article[index[0]:index[1]]
    cnt+=1
print "Number of matches: "
print cnt


kitten]]''. the male progenitor of a cat, especially a pedigreed cat, is its ''sire'',<ref>{{cite web|url=http://www.oed.com/view/entry/180366?rskey=yylu4e&result=1&isadvanced=false#eid|title=sire|work=the oxford
(27956, 28204)


# In[78]:

import csv

query = "'cat' (0,10) 'are' (0,10) 'to'"

startTime = datetime.now()
cnt = 0
csv_matches = []
with open('cat_article.csv','r') as CSV:
    articles = csv.reader(CSV)
    for row in articles:
        matches = check_wiki(row[1],query)
        if(matches != False):
            for index in matches:
                print index 
                print row[1][index[0]:index[1]]

finishingTime = datetime.now() - startTime

print finishingTime

#for index in matches:
#    print index 
#    print article[index[0]:index[1]]


# In[108]:

import sys
import csv

csv.field_size_limit(sys.maxsize)

#query = "'cat' (0,10) 'are' (0,10) 'to'"

query = "'arnold' (0,10) 'schwarzenegger' (0,10) 'is'"

startTime = datetime.now()
cnt = 0
csv_matches = []
with open('a_articles.csv','r') as CSV:
    articles = csv.reader(CSV)
    for row in articles:
        cnt+=1
        matches = check_wiki(row[1],query)
        if(matches != False):
            [csv_matches.append(row[1][index[0]:index[1]]) for index in matches]
    finishingTime = datetime.now() - startTime
    print finishingTime

print csv_matches


# In[109]:

import sys
import csv

csv.field_size_limit(sys.maxsize)

#query = "'cat' (0,10) 'are' (0,10) 'to'"

query = "'elephants' (0,20) 'are' (0,20) 'to'"

startTime = datetime.now()
cnt = 0
csv_matches = []
with open('articles.csv','r') as CSV:
    articles = csv.reader(CSV)
    for row in articles:
        cnt+=1
        matches = check_wiki(row[1],query)
        if(matches != False):
            [csv_matches.append(row[1][index[0]:index[1]]) for index in matches]
    finishingTime = datetime.now() - startTime
    print finishingTime
    
print csv_matches


# In[110]:

print(len(csv_matches))


# In[ ]:



