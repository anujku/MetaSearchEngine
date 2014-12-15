import cPickle

dil = open("avgdoclen.p", "r")
p = cPickle.Unpickler(dil)
avgdoclen = p.load()

dil = open("termids.p", "r")
p = cPickle.Unpickler(dil)
termids = p.load()

dil = open("totalterms.p", "r")
p = cPickle.Unpickler(dil)
totalterms = p.load()

dil = open("uniqueterms.p", "r")
p = cPickle.Unpickler(dil)
uniqueterms = p.load()

dil = open("doclengths.p", "r")
p = cPickle.Unpickler(dil)
doclengths = p.load()

dil = open("termoffsets.p", "r")
p = cPickle.Unpickler(dil)
termoffsets = p.load()

dil = open("termctfdf.p", "r")
p = cPickle.Unpickler(dil)
termctfdf = p.load()

dil = open("termidf.p", "r")
p = cPickle.Unpickler(dil)
termidf = p.load()

dil = open("stopwords.p", "r")
p = cPickle.Unpickler(dil)
stopwords = p.load()

from porterstemmer import *
PStemmr = PorterStemmer()

def stem(word):
    return PStemmr.stem(word.lower(), 0, len(word)-1)

def invlist(word):
    word = stem(word)
    if word not in termids:
        return {}        
    termid = termids[word]
    offset = termoffsets[termid]
    with open('bigfile.txt') as f:
        f.seek(offset)
        temp = ''
        c = ''
        while c != '|':
            c = f.read(1)
            temp = temp + str(c)
        temp = temp.strip('|')
        temp = temp.split()
        temphash = {}
        for i in xrange(0,len(temp)/2):
            temphash[temp[i*2]] = float(temp[(i*2)+1])
        return temphash
            
def getctfdf(word):
    word = stem(word)
    if word not in termids:
        return {'0','0'}
    else:
        return termctfdf[str(termids[stem(word)])]
    
def stopnstem(query):
    stopnstemmed = []
    terms = query.split()
    for term in terms:
        if term.lower() not in stopwords:
            term = stem(term)
            stopnstemmed.append(term)
    return stopnstemmed

def getidf(word):
    if stem(word) in termids:
        return termidf[termids[stem(word)]]
    else:
        return 0.0

def getctf(word):
    if stem(word) in termids:
        return termctfdf[termids[stem(word)]][0]
    else:
        return 0
    
def getdf(word):
    if stem(word) in termids:
        return termctfdf[termids[stem(word)]][1]
    else:
        return 0

#print getidf('algebra')
#print stopnstem('arithmetic is a funny Language')
#print invlist('CA620725')
#print getctfdf('arithmetic')
#print doclengths
#print termctfdf
#print termids