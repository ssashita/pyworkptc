#!/cygdrive/d/sachin/cygwin/bin/python
import sys
import re

#This script can take several file names as arguments. The files are expected to
#contain Clearcase FILE/DIRECTORY element strings. Typically these files contain the 
#list of files that a NCST submission picks up based on element trace id = submission id. 
# The order of the input files is also typically from the file for the oldest submission 
# to the latest.
# The first part of the output from this script is a list of 
#elements that are a kind of union of elements in all the files, such that only 
#the latest version of any element is in the union. This list is followed 
#by two integers, which are not so important. Finally the output has a list of 
# elements that are in the union of (latest-version) elements in all the files,
 #minus the ones in the last input file.
# The assumption made by the script is that
#if a FILE/DIRECTORY element is present multiple times in possibly several 
#input files, then it is from 
#the same Clearcase branch in all. In our case the input files typically 
#contain a list of 
#Clearcase elements which all belong to a branch path with the same ending 
# branch viz. "sync_cainteg.x-24-mor", our CC 'staging' branch. Also, we probably 
#won't have DIRECTORY elements in the  
#files  because everything copied to the sync_cainteg.x-24-mor branch is coming 
#from GIT
def main() :
    #print 'Number of arguments:', len(sys.argv), ' arguments'
    #print 'Argument List:', str(sys.argv)
    
    listOfNameVersionPairs = list()
    prevNameVersionDict= None
    for file in sys.argv[1:] :
        nameVersionDict = dict()
        #listOfNameVersionPairs.append(nameVersionDict)
        f=open(file,"r")
        contents = f.read()
        nameVersions = re.split("\s",contents)
        #dumpNameversion(nameVersions)
        populateNameVersionDict(nameVersions,nameVersionDict)
        #print nameVersionDict
        if prevNameVersionDict is None:
            prevNameVersionDict = nameVersionDict
            continue
        prevNameVersionDict,differenceVersionsDict, hitcount,overridecount = mergeDicts(prevNameVersionDict,nameVersionDict )
    for name in prevNameVersionDict:
        print name + prevNameVersionDict[name][1]
    print '----------------------------------------------------------------------------------------------'
    print '----------------------------------------------------------------------------------------------'
    print 'final hitcount is ' + str(hitcount)
    print 'final overridecount is ' + str(overridecount)
    print '----------------------------------------------------------------------------------------------'
    print '----------------------------------------------------------------------------------------------'
    for name in differenceVersionsDict:
        print name + differenceVersionsDict[name][1]


#return the union of latest version elements from prevdict and currdict
#
def mergeDicts(prevdict, currdict):
    resultdict =dict()
    diffVersionsDict =dict()
    hitcount=0
    overridecount=0
    for name in currdict:
        if name in prevdict:
            hitcount=hitcount+1
            if currdict[name][0] > prevdict[name][0]:
                resultdict[name] = currdict[name]
                overridecount=overridecount+1
            else:
                resultdict[name] = prevdict[name]
        else:
            resultdict[name] = currdict[name]
    for name in prevdict:
        if name not in resultdict:
            diffVersionsDict[name] =  prevdict[name]
            resultdict[name] = prevdict[name]
    return resultdict,diffVersionsDict,hitcount,overridecount
 
# Split every fully qualified Clearcase element path in the list nameVers, and
# populate the dictionary, nvdict, with the element OS path as key and the value as 
# a 2-tuple which has version number as first element, the second element being the portion 
#of the fully qualified path starting from "@@" to the end         
def populateNameVersionDict(nameVers,nvdict):
    for nv in nameVers:
        if re.match("\s",nv) or ""==nv:
            continue
        #print nv
        pos = nv.find(r'@@',0)
        name = nv[:pos]
        version=nv[pos+2:]
        #print name + " " + version
        version=version[::-1] # reverse it
        end=version.find('/',0)
        version = version[0:end]
        version=version[::-1] # reverse it
        nvdict[name]=version, nv[pos:]

def dumpNameversion(nameVers):
    for nv in nameVers:
        print nv


if __name__ == "__main__":
    main()
