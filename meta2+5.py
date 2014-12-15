import cPickle, time, math
t0 = time.clock(
                )
dil = open("bm25scores.p", "r")
p = cPickle.Unpickler(dil)
bm25scores = p.load()

dil = open("tfidfscores.p", "r")
p = cPickle.Unpickler(dil)
tfidfscores = p.load()

dil = open("qnums.p", "r")
p = cPickle.Unpickler(dil)
qrynums = p.load()

dil = open("queryarray.p", "r")
p = cPickle.Unpickler(dil)
queries = p.load()

print time.clock() - t0
print "All Pickles loaded"

from operator import itemgetter
bm25sorted = [None]*len(queries)
tfidfsorted = [None]*len(queries)

bm25normed = [[None]]*len(queries)
tfidfnormed = [[None]]*len(queries)

sortedcomboscore = [None]*len(queries)


for q in xrange(0,len(queries)):
    bm25sorted[q] = sorted(bm25scores[q].items(), key=itemgetter(1), reverse=True)
    tfidfsorted[q] = sorted(tfidfscores[q].items(), key=itemgetter(1), reverse=True)
    bm25max = bm25sorted[q][0][1]
    tfidfmax = tfidfsorted[q][0][1]
    comboscore = {}
    for doc in bm25scores[q]:
        print doc
        comboscore[doc] = (bm25scores[q][doc]/bm25max) + (tfidfscores[q][doc]/tfidfmax)
    sortedcomboscore[q] = sorted(comboscore.items(), key=itemgetter(1), reverse=True) 


myfile = file("output2+5.txt", 'w')
for q in xrange(0,len(queries)):
    rank = 1
    for i in xrange(0,min(1000,len(sortedcomboscore[q]))):
        print >> myfile, str(qrynums[q]) + " Q0 CACM-"+ str(sortedcomboscore[q][i][0]) +" "+ str(rank) +" "+ str(sortedcomboscore[q][i][1]) + " Exp" 
        rank = rank + 1

print time.clock() - t0
print "All Scores Sorted and Normalized"

