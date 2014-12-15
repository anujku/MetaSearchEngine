from lemur_api import *
import re

queryfile = 'C:\Users\FRANCIS\keithxm23_eclipse_workspace\IR Term Project\cacm_glasgow\query_manual.text'
f = open(queryfile, 'r')
lines = f.readlines()
f.close()

qnums = []
queryarray = [None]*64
for line in lines:
    terms = line.split()
    if len(terms) == 0:
        continue
    if terms[0] == '.I':
        query = ""
#        print "Start of document: " + str(terms[1])
        eof = False
        querynum = int(terms[1])
        qnums.append(querynum)
    elif terms[0] == '.N':
#        print "qnum is " + str(querynum)
        queryarray[querynum-1] = query
#        print "End of document: " + str(docid)       
        eof = True
    elif terms[0] == '.W' or terms[0] =='.A':
#        print "found T/A/B/N in doc: " + str(docid)
        pass
    elif eof == False:
        words = re.findall(r'\w+', line)
#        print words
        query+= ' ' + ' '.join(words)
        
#for q in queryarray:
#    print stopnstem(q)

import cPickle
   
fil = open("qnums.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(qnums)
fil.close()
   
fil = open("queryarray.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(queryarray)
fil.close()