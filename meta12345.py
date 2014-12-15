import cPickle, time, math
t0 = time.clock()

dil = open("okapiscores.p", "r")
p = cPickle.Unpickler(dil)
okapiscores = p.load()
dil = open("tfidfscores.p", "r")
p = cPickle.Unpickler(dil)
tfidfscores = p.load()
dil = open("lapscores.p", "r")
p = cPickle.Unpickler(dil)
lapscores = p.load()
dil = open("jeliscores.p", "r")
p = cPickle.Unpickler(dil)
jeliscores = p.load()
dil = open("bm25scores.p", "r")
p = cPickle.Unpickler(dil)
bm25scores = p.load()
dil = open("qnums.p", "r")
p = cPickle.Unpickler(dil)
qrynums = p.load()
dil = open("queryarray.p", "r")
p = cPickle.Unpickler(dil)
queries = p.load()

#print time.clock() - t0
#print "All Pickles loaded"

from operator import itemgetter

bm25sorted = [None]*len(queries)
tfidfsorted = [None]*len(queries)
okapisorted = [None]*len(queries)
lapsorted = [None]*len(queries)
jelisorted = [None]*len(queries)

bm25normed = [[None]]*len(queries)
tfidfnormed = [[None]]*len(queries)
okapinormed = [None]*len(queries)
lapnormed = [None]*len(queries)
jelinormed = [None]*len(queries)

sortedcomboscore = [None]*len(queries)

for q in xrange(0,len(queries)):
    bm25sorted[q] = sorted(bm25scores[q].items(), key=itemgetter(1), reverse=True)
    tfidfsorted[q] = sorted(tfidfscores[q].items(), key=itemgetter(1), reverse=True)
    okapisorted[q] = sorted(okapiscores[q].items(), key=itemgetter(1), reverse=True)
    lapsorted[q] = sorted(lapscores[q].items(), key=itemgetter(1), reverse=True)
    jelisorted[q] = sorted(jeliscores[q].items(), key=itemgetter(1), reverse=True)
    
    bm25max = bm25sorted[q][0][1]
    tfidfmax = tfidfsorted[q][0][1]
    okapimax = okapisorted[q][0][1]
    lapmax = lapsorted[q][0][1]
    jelimax = jelisorted[q][0][1]
    
    
    bm25coef = 0.3507
    okapicoef = 0.2612/bm25coef
    tfidfcoef = 0.3356/bm25coef
    lapcoef = 0.2614/bm25coef
    jelicoef = 0.2114/bm25coef
    bm25coef = 1.0
    
    
    
    comboscore = {}
    for doc in bm25scores[q]:
        
        if bm25max == 0:
            bm25 = 0
        else:
            bm25 = bm25coef*bm25scores[q][doc]/bm25max
        if tfidfmax == 0:
            tfdf = 0
        else:
            tfidf = tfidfcoef*tfidfscores[q][doc]/tfidfmax
        if okapimax == 0:
            okapi = 0
        else:
            okapi = okapicoef*okapiscores[q][doc]/okapimax
        if lapmax == 0:
            lap = 0
        else:
            lap = lapcoef*lapscores[q][doc]/lapmax
        if jelimax == 0:
            jeli = 0
        else:
            jeli = jelicoef*jeliscores[q][doc]/jelimax
                
        comboscore[doc] = bm25 + tfidf + lap + jeli #+ okapi
    sortedcomboscore[q] = sorted(comboscore.items(), key=itemgetter(1), reverse=True) 


myfile = file("output12345.txt", 'w')
for q in xrange(0,len(queries)):
    rank = 1
    for i in xrange(0,min(1000,len(sortedcomboscore[q]))):
        print >> myfile, str(qrynums[q]) + " Q0 CACM-"+ str(sortedcomboscore[q][i][0]) +" "+ str(rank) +" "+ str(sortedcomboscore[q][i][1]) + " Exp" 
        rank = rank + 1

print time.clock() - t0
print "All Scores Sorted and Normalized"

