import os, cPickle, time, math

t0 = time.clock()

#terms directory
termsfolder = 'C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/terms'

dil = open("doclengths.p", "r")
p = cPickle.Unpickler(dil)
doclengths = p.load()

termoffsets = {}
termids = {}

#change working directory to corpus so as to facilitate walking through all of the files
os.chdir(termsfolder)

invindexpath = 'C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/bigfile.txt'

#deleting old term files
try:    
    if os.path.isfile(invindexpath):
        os.unlink(invindexpath)
except Exception, e:
    print e
    
    
f2 = open(invindexpath, 'a')

termctfdf = {}
termidf = {}
for subdir, dirs, files in os.walk(termsfolder):
    for file in files:
        print "Parsing file: " + file
        f = open(file, 'r')
        line = f.readlines()
        line = line[0] #since the file contains only a single line
        f.close()
        
        word = file[1:-4]
        termids[word] = f2.tell()
        termid = termids[word]
        termoffsets[termid] = f2.tell()
        terms = line.split()
        ctf = len(terms)
#            print terms
        temptermhash = {}
        for term in terms:
            temptermhash[term] = terms.count(term) #so as to avoid writing for same document occurency multiple times
        termctfdf[termid] = [ctf,len(temptermhash)]
        termidf[termid] = math.log(len(doclengths)/len(temptermhash))
        for key in temptermhash:
            f2.write(str(key) + ' ' + str(temptermhash[key]) + ' ')
        f2.write('| ')
f2.close()

#print termoffsets
#print termctfdf
fil = open("C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/termoffsets.p", "w")   
p = cPickle.Pickler(fil)
p.dump(termoffsets)
fil.close()

fil = open("C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/termids.p", "w")   
p = cPickle.Pickler(fil)
p.dump(termids)
fil.close()

fil = open("C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/termctfdf.p", "w")   
p = cPickle.Pickler(fil)
p.dump(termctfdf)
fil.close()

fil = open("C:/Users/FRANCIS/keithxm23_eclipse_workspace/IR Term Project/termidf.p", "w")   
p = cPickle.Pickler(fil)
p.dump(termidf)
fil.close()

print time.clock() - t0