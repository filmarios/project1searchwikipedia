import re
import csv
import sys

# the maximum csv field size has to be set to max to contain the long strings specified in the assignment.
csv.field_size_limit(sys.maxsize)
# transform the parse string to something useful, two lists.
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
# example: if the word cat is followed by two instances of the word hat, and they are within range, the list would be [1,1]
def matches_count(indexes,word_length,words,matches):
    matches_count = matches
    # iterate the matches list rows
    for row in range(len(words)-1):
        # iterate the matches list columns
        for col in range(len(matches[row])):
            # create a range from the given indexes, to see if the next word is within that range.
            newRange = range(indexes[row][0]+matches[row][col]+word_length[row],
                             indexes[row][1]+matches[row][col]+word_length[row])
            # Check for each entry of the nex row, if there is a match between that word and the range.
            matches_count[row][col] = [1 if x in newRange else 0 for x in matches[row+1]]
    return matches_count

# generate a list of matches for each string
def matching_string_indexes(words,matches_count,matches):
    # empty list to store the final matches between first and last strings.
    fin_match = []
    # iterate the columns of matches_count
    for col in range(len(matches_count[0])):
        # start at the top "layer" of the matches, that is, for the first string
        layer = 0
        # indexing for the next layer is made, checking if the match value is in fact 1.
        index = [ind for ind, value in enumerate(matches[layer][col]) if value == 1]
        # start at layer 1.
        for layer in range(1,len(words)):
            match_lists = [matches[layer][i] for i in index]
            index = []
            
            # the bottom layer has not yet been reached, try to 
            if (layer < len(words)-1):
                for match in match_lists:
                    ind = [ind for ind, value in enumerate(match) if value == 1]
                    index = index + ind
            else:
                fin_match.append(match_lists)
    return fin_match

def check_wiki(words,indexes,word_length,article,query):
    # if the strings are all present in the article.
    
    if (all_strings_exist(words,article)==True):
        
        mtch = index_of_words(word_length,words,article)
        mtch_cnt = matches_count(indexes,word_length,words,mtch)
        fin_match = matching_string_indexes(words,mtch_cnt,mtch)
        index_start = [word.start() for word in re.finditer(words[0],article)]
        match_indexes=[]
        for i in range(len(index_start)):
            if (sum(fin_match[i])!=0):
                for n in range(len(fin_match[i])):
                    match_indexes.append((index_start[i],fin_match[i][n]+word_length[-1]))
        return match_indexes
    else:
        return False    

### Example of use with the whole wikipedia csv ###

query = "'elephants' (0,20) 'are' (0,20) 'to'"
ARTICLE = 'articles.csv'

words, indexes, word_length = parse_query(query)
matching_strings = []

with open(ARTICLE,'r') as CSV:
    articles = csv.reader(CSV)
    for row in articles:
        matches = check_wiki(words,indexes,word_length,row[1],query)
        if(matches != False):
            for index in matches:
                matching_strings.append(row[1][index[0]:index[1]])
                
for string in matching_strings:
    print string
