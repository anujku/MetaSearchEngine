from lemur_api import *
import time, math
t0 = time.clock()

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

print time.clock() - t0
print "caclulated query vectors"

docvectors = [None]*len(queries)
for q in xrange(0, len(queries)):
    seendocs = {}
    terms = stopnstem(queries[q])
    for i in xrange(0,len(terms)):
        terminvlist = invlist(terms[i])
        for doc in terminvlist:                        
            tf = terminvlist[doc]
            if doc in seendocs:
                seendocs[doc][i] = tf*getidf(terms[i])/(tf+k+c*(doclengths[doc]/avgdoclen))
            else:
                seendocs[doc] = [0.0]*len(terms)
                seendocs[doc][i] = tf*getidf(terms[i])/(tf+k+c*(doclengths[doc]/avgdoclen))
    docvectors[q] = seendocs
    
print time.clock() - t0
print "caclulated docvectors"  

queryscores = [None]*len(queries)
#calculating scores of each document
for q in xrange(0,len(queries)):
    terms = stopnstem(queries[q])
    docscores = {}
    docs = docvectors[q]
    for doc in docs:
        numerator = 0.0
        xsqr = 0.0
        ysqr = 0.0
        vector = docs[doc]
        for i in xrange(len(vector)):
            numerator += vector[i]*queriesokapi[q][i]
            xsqr += vector[i]*vector[i]
            ysqr += queriesokapi[q][i]*queriesokapi[q][i]
        denominator = math.sqrt(xsqr + ysqr)
        if denominator == 0.0:
            docscores[doc] = 0.0
        else:
            docscores[doc] = numerator/denominator
    queryscores[q] = docscores

print time.clock() - t0
print "caclulated scores by cosine product"
       
#now rank the scores
from operator import itemgetter

myfile = file("output2.txt", 'w')
sortedscores = [None]*len(queries)
for q in xrange(0,len(queries)):
    sortedscores[q] = sorted(queryscores[q].items(), key=itemgetter(1), reverse=True)
    rank = 1
    for i in xrange(0,min(1000,len(sortedscores[q]))):
        print >> myfile, str(qrynums[q]) + " Q0 CACM-"+ str(sortedscores[q][i][0]) +" "+ str(rank) +" "+ str(sortedscores[q][i][1]) + " Exp" 
        rank = rank + 1

print time.clock() - t0

import cPickle   
fil = open("tfidfscores.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(queryscores)
fil.close()