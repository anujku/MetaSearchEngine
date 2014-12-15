from lemur_api import *

k=0.5
c=0.25

dil = open("qnums.p", "r")
p = cPickle.Unpickler(dil)
qrynums = p.load()

dil = open("queryarray.p", "r")
p = cPickle.Unpickler(dil)
queries = p.load()


queriesokapi = [None]*len(queries)
relevantdocs = [None]*len(queries)
for q in xrange(0, len(queries)):
    terms = stopnstem(queries[q])
    #Calculate Query's Okapi TF
    qryokapi = [None]*len(terms)
    docsseen = {}
    for i in xrange(0,len(terms)):
#        print invlist(terms[i])
        docsseen.update(invlist(terms[i]))
        tf = terms.count(terms[i])
        qryokapi[i] = tf/(tf+k+c*(len(terms)/avgdoclen))
    queriesokapi[q] = qryokapi
    relevantdocs[q] = docsseen
    
docvectors = [None]*len(queries)
for q in xrange(0, len(queries)):
    seendocs = {}
    terms = stopnstem(queries[q])
    for i in xrange(0,len(terms)):
        terminvlist = invlist(terms[i])
        for doc in terminvlist:                        
            tf = terminvlist[doc]
            if doc in seendocs:
                seendocs[doc][i] = tf/(tf+k+c*(doclengths[doc]/avgdoclen))
            else:
                seendocs[doc] = [0.0]*len(terms)
                seendocs[doc][i] = tf/(tf+k+c*(doclengths[doc]/avgdoclen))
    docvectors[q] = seendocs

queryscores = [None]*len(queries)
#calculating scores of each document
for q in xrange(0,len(queries)):
    docscores = {}
    docs = docvectors[q]
    for doc in docs:
        score = 0.0
        vector = docs[doc]
        for i in xrange(len(vector)):
            score += vector[i]*queriesokapi[q][i]
        docscores[doc] = score
    queryscores[q] = docscores
        
#now rank the scores
from operator import itemgetter

myfile = file("output1.txt", 'w')
sortedscores = [None]*len(queries)
for q in xrange(0,len(queries)):
    sortedscores[q] = sorted(queryscores[q].items(), key=itemgetter(1), reverse=True)
    rank = 1
    for i in xrange(0,min(1000,len(sortedscores[q]))):
        print >> myfile, str(qrynums[q]) + " Q0 CACM-"+ str(sortedscores[q][i][0]) +" "+ str(rank) +" "+ str(sortedscores[q][i][1]) + " Exp" 
        rank = rank + 1


import cPickle   
fil = open("okapiscores.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(queryscores)
fil.close()