from xml.dom import minidom
import os
import glob
import collections
import string
import time
import re


from porter_stemmer_tartarus import PorterStemmer

#path = 'Relative path for using datafile'
path = 'Cranfield/*'

startTime = time.time()
files = glob.glob(path)
#tokens list to store tokens
tokenList = []
#Given below code generates tokens from text 
for i, file in enumerate(files):
    doc = minidom.parse(file)
    textNode = doc.getElementsByTagName("TEXT")
    textChild=textNode[0].firstChild
    text = textChild.nodeValue
    textList = text.splitlines()

    for textIndex in textList:
        textPunc = re.sub(r'[^a-zA-Z0-9\s]', '', textIndex)
        tokensList = textPunc.split(" ")
		#List to remove null tokens and numeric tokens from tokensList
        filteredTokenList = [token for token in tokensList if token != '' and not token.isnumeric()]
        for token in filteredTokenList:
            tokenList.append(token)


print('The total number of tokens:\n', len(tokenList), 'tokens')
print('The number of unique tokens:', len(set(tokenList)))

numOfTokens = collections.Counter(tokenList)
uniqueTokens = [word for word, numOfTokens in numOfTokens.items() if numOfTokens==1]
print('The number of words with single appearence:', len(uniqueTokens))
top30 = collections.Counter(tokenList).most_common(30)
print('30 most frequent words and their respective frequency:')
for token in top30:
    print(token)
print('Avg number of tokens per document:', round(len(tokenList)/len(files), 2))

print()

porterStemmer = PorterStemmer()
stems = [porterStemmer.stem(token, 0, len(token)-1) for token in tokenList]
print('The number of different stems:', len(set(stems)))
stemCounts = collections.Counter(stems)
uniqueStems = [stem for stem, count in stemCounts.items() if count==1]
print('The number of stems with single appearence:', len(uniqueStems))
top30stems = stemCounts.most_common(30)
print('30 most frequent stems with their respective frequencies:') 
for stem in top30stems:
    print(stem)  
print('Avg number of word-stems per document:', round(len(stems)/len(files),2))
print(time.time()-startTime)