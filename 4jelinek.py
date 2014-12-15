from lemur_api import *
import time
t0 = time.clock()

lmbda = 1.0

dil = open("qnums.p", "r")
p = cPickle.Unpickler(dil)
qrynums = p.load()

dil = open("queryarray.p", "r")
p = cPickle.Unpickler(dil)
queries = p.load()

relevantdocs = [None]*len(queries)
for q in xrange(0, len(queries)):
    terms = stopnstem(queries[q])
    docsseen = {}
    for i in xrange(0,len(terms)):
#        print invlist(terms[i])
        docsseen.update(invlist(terms[i]))
    relevantdocs[q] = docsseen
    
print str(time.clock() - t0) + " -- found relevant documents set"


queryscores = [None]*len(queries)
#calculating scores of each document
for q in xrange(0,len(queries)):
    docscores = {}
    terms = stopnstem(queries[q])
    for i in xrange(len(terms)):
        terminvlist = invlist(terms[i])
        ctf = getctf(terms[i])
        for doc in relevantdocs[q]:
            if i == 0:
                docscores[doc] = 1.0
            if doc in terminvlist:
                docscores[doc] *= ((lmbda*terminvlist[doc]/doclengths[doc]) + ((1.0 - lmbda)*ctf/totalterms))
            else:
                docscores[doc] *= (1.0 - lmbda)*ctf/totalterms
    queryscores[q] = docscores

    
print str(time.clock() - t0) + " -- calculated scores"
        
#now rank the scores
from operator import itemgetter

myfile = file("output4.txt", 'w')
sortedscores = [None]*len(queries)
for q in xrange(0,len(queries)):
    sortedscores[q] = sorted(queryscores[q].items(), key=itemgetter(1), reverse=True)
    rank = 1
    for i in xrange(0,min(1000,len(sortedscores[q]))):
        print >> myfile, str(qrynums[q]) + " Q0 CACM-"+ str(sortedscores[q][i][0]) +" "+ str(rank) +" "+ str(sortedscores[q][i][1]) + " Exp" 
        rank = rank + 1

print time.clock() - t0


import cPickle   
fil = open("jeliscores.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(queryscores)
fil.close()