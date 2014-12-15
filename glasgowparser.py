import os, cPickle, re, time
t0 = time.clock()

#corpus directory
corpus = 'C:\Users\FRANCIS\keithxm23_eclipse_workspace\IR Term Project\cacm_glasgow\cacm.all'

#load pickled stopwords.. source: stopper.py
dil = open("stopwords.p", "r")
p = cPickle.Unpickler(dil)
stopwords = p.load()


from porterstemmer import *
PStemmr = PorterStemmer()

#check if folder exists if not create it
folder = 'C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/terms'
if not os.path.exists(folder):
    os.makedirs(folder)

#First delete all previous term txt files if any
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception, e:
        print e
#finished deleting
print time.clock() - t0
print "all old term files deleted"
    


doclengths = {}
seenwords = {}
uniqueterms = 0
totalterms = 0

#load cacm corpus into memory
f = open(corpus, 'r')
lines = f.readlines()
f.close()

eof = False #end of file -flag
#cycle through every line
for line in lines:
    terms = line.split()
    if terms[0] == '.I':
#        print "Start of document: " + str(terms[1])
        doclen = 0
        eof = False
        docid = terms[1]
    elif terms[0] == '.N':
#        print "End of document: " + str(docid)
        doclengths[str(docid)] = doclen        
        eof = True
    elif terms[0] == '.T' or terms[0] =='.A' or terms[0] =='.B':
#        print "found T/A/B/N in doc: " + str(docid)
        pass
    elif eof == False:
        words = re.findall(r'\w+', line)
        for word in words:
            word = word.lower()
            if word not in stopwords:
                totalterms+=1
                doclen += 1
#                print "Did NOT stopword: " + word
                word = PStemmr.stem(word, 0, len(word)-1)
#                print "Stemmed to: " + PStemmr.stem(word, 0, len(word)-1)
                termpath = 'terms/z' + word + str('.txt')
                if word not in seenwords:
                    seenwords.update({word:None})
                    uniqueterms+=1                        
                x2 = open(termpath, 'a')
                x2.write(' ' + str(docid))
                x2.close()
            
print time.clock() - t0

avgdoclen = 0.0
for docs in doclengths:
    avgdoclen += doclengths[docs]
avgdoclen /= len(doclengths)

#print avgdoclen
#print seenwords
#print len(doclengths)
#print uniqueterms
#print len(termids)
#print totalterms

import cPickle
   
fil = open("doclengths.p", "w")   
p = cPickle.Pickler(fil) 
p.dump(doclengths)
fil.close()


fil1 = open("uniqueterms.p", "w")   
p1 = cPickle.Pickler(fil1) 
p1.dump(uniqueterms)
fil1.close()

fil3 = open("totalterms.p", "w")   
p3 = cPickle.Pickler(fil3) 
p3.dump(totalterms)
fil3.close()
