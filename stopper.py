stopwords = {}
f=open("stoplist.txt")
for line in f.readlines():
    line = line.strip("\n")
    stopwords[line] = None
f.close()

import cPickle
   
fil = open("stopwords.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(stopwords)
fil.close()