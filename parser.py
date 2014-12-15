import os, cPickle, re, time
t0 = time.clock()

#corpus directory
rootdir = 'C:\Users\FRANCIS\keithxm23_eclipse_workspace\IR Term Project\minicacm'

#load pickled stopwords.. source: stopper.py
dil = open("stopwords.p", "r")
p = cPickle.Unpickler(dil)
stopwords = p.load()

#change working directory to corpus so as to facilitate walking through all of the files
os.chdir(rootdir)

#import Porter Stemmer from porterstemmer.py
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

doclengths = {}
termids = {}
uniqueterms = 0

#now create fresh term files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        AMPMflag = False
        doclen = 0
#        print "Parsing file: " + file
        f = open(file, 'r')
        lines = f.readlines()
#        print lines
        f.close()
        for line in lines:
            if AMPMflag == True:
                break
            line = line.replace('<html>', '').replace('<pre>', '').replace('</pre>', '').replace('</html>', '')
#            print line
            terms = re.findall(r'\w+', line)
            for term in terms:
                if (term == 'AM' or term == 'PM'):
                    AMPMflag = True #to remove the bibliographic references that follow the AM or PM word
                    break
                term = term.lower()
                if term in stopwords:
                    pass
#                    print "stopworded the term: " + term
                else:
                    doclen += 1
#                    print "Did NOT stopword: " + term
                    term = PStemmr.stem(term, 0, len(term)-1)
#                    print "Stemmed to: " + PStemmr.stem(term, 0, len(term)-1)
                    if term in termids:
                        tid = termids[term]
                        termpath = '../terms/' + str(tid) + str('.txt')
                    else:
                        uniqueterms+=1
                        termids[term] = uniqueterms
                        termpath = '../terms/' + str(uniqueterms) + str('.txt')                        
                    x2 = open(termpath, 'a')
                    x2.write(' ' + str(file[5:9]))
                    x2.close()
        doclengths[str(file[5:9])] = doclen
#finished creating term txt files

print time.clock() - t0

print len(doclengths)
print uniqueterms
print len(termids)