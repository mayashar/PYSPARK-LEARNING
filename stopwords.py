# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 13:35:12 2019

@author: HP
"""

import glob
import errno
import itertools
import re
import operator

# Input files, all files in same directory
path = '*.txt'
#take all the files from same directory
files = glob.glob(path)

st = open('stopwords.txt', 'r')
lines = st.readlines()
stopwords = '\t'.join([line.strip() for line in lines])

#Output of reduce
reduce_output = {}
#====================================================================
#convert to lowerccase and remove stopwords
#====================================================================
def preprocessor(text):
    
    text_list = []
 
    keep_list = []
    
    
    text_list = re.findall(r'\w+', text.lower())
    
    
    
    for word in text_list: 
     if word not in stopwords: 
       keep_list.append(word)
    
    return keep_list

#===================================================================
# Map Function 
#===================================================================
def map(id,files):
    preprocessed_text=[]
    
    for name in files:
        try:
            with open(name) as f:
                pass 

                text = f.read()
                preprosess_op = preprocessor(text) 
                
                preprocessed_text.append(preprosess_op)

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    
    
    i=0
    j=0
    word_dictionary = {}  
    
    for i in range(len(preprocessed_text)):
        for j in range(len(preprocessed_text[i])):
            
            temp_list = [i+1,1]
            if preprocessed_text[i][j] in word_dictionary:
              word_dictionary[preprocessed_text[i][j]].append(temp_list)
            else:
              word_dictionary[preprocessed_text[i][j]] = [temp_list]
    
    
    return word_dictionary    


#===================================================================
# Reduce Function
#===================================================================
def reduce(word_dictionary):
    for k in word_dictionary:
        values = word_dictionary.get(k)  
           
        if(len(values)==1):
            reduce_output[k]=values 
        else: 
            merge_count = []  
            already_visited = []
            for key,val in values:
                if [key,val] not in already_visited: 
                    merge_count.append([key,values.count([key,val])])
                 
                if [key,val] not in already_visited:
                    already_visited.append([key,val])
            reduce_output[k]=merge_count
    

#===================================================================
# Search Function
#===================================================================           
def search(user_input):
    
    search_op = []
    preprocess_op = preprocessor(user_input)
    
    for word in preprocess_op:
        if word in reduce_output:
            print("\t",word," - Found")
            temp = reduce_output[word]
            search_op.append(temp)
           
        else:
            print("\t",word," - Not Found")  
    
    
    flattened_list  = list(itertools.chain(*search_op))
    count={}
    for k,v in flattened_list:
         if k in count:
             count[k] += v
         else:
             count[k]=v
                
    rank_sorting = sorted(count.items(),key=operator.itemgetter(1),reverse=True)
    print("\n Final Search Output: ",rank_sorting)
    
   
if __name__ == '__main__':
    
    #Map function
    map_output=map(0,files)
    
    #Reduce Function
    reduce(map_output)
    
    #Accept string input from USER 
    user_input = input("\n Enter the string to search in Files: ")
    
    #Search Function
    search(user_input)


#============================================================================

# end of map reduce without lambda

#===========================================================================
#with lambda function
#==========================================================================
st = open('stopwords.txt', 'r')
lines = st.readlines()
stopwords = '\t'.join([line.strip() for line in lines])

st1 = open('01.txt.txt', 'r')
lines1 = st1.readlines()
txt01 = '\t'.join([line.strip() for line in lines1]) 
st2 = open('02.txt.txt', 'r')
lines2 = st2.readlines()
txt02 = '\t'.join([line.strip() for line in lines1])                   
                    

lower_list = []

filtered_list = []
lower_list= txt02.lower().split()
for w in lower_list: 
     if w not in stopwords: 
       filtered_list.append(w)
    


from functools import reduce
from operator import add

def number_of_words(s):
    words = s.split(' ')
    return len(words)

counts = map(number_of_words, filtered_list)
total = reduce(add, counts)
lambda x: len(x.split(' '))
total_txt01 = reduce(add, map(lambda x: len(x.split(' ')), filtered_list))
