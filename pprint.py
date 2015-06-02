#!/d/python27/python
import sys
import re

def main() :
    #print 'Number of arguments:', len(sys.argv), ' arguments'
    #print 'Argument List:', str(sys.argv)
    
    for file in sys.argv[1:] :
        f=open(file,"r")
        contents = f.read()
        nameVersions = re.split("\s",contents)
        for line in nameVersions:
            if not re.match("\s",line ):
                print line
  

def dumpNameversion(nameVers):
    for nv in nameVers:
        print nv


if __name__ == "__main__":
    main()
