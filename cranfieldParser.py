from collections import Counter 
import glob, os, re 
from collections import defaultdict    
import nltk 
import sys  

def read_file(filename):
    infile = open(filename) 
    contents = infile.read()
    infile.close()
    return contents  


import io
begtext = '<TEXT>\n'  
endtext = '\n</TEXT>' 

for i in range(1,1401):  
    n = str(i)
    curName = "data/CranfieldDocs/cranfield" +  str(n.rjust(4, '0'))
    text = read_file(str("data/CranfieldDocs/cranfield" + str(n.rjust(4,'0')))) 
    start =  text.find(begtext) 
    end =  text.find(endtext)  
    start += 8
    text2 = text[start:end]  
    with io.open("data/CranfieldDocsParse/parsed" + str(n.rjust(4,'0')) + ".txt", 'wb') as f: 
        f.write(text2) 
    i += 1 


