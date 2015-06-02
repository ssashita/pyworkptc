#!/cygdrive/d/sachin/cygwin/bin/python
import sys
#from os import *
import os

def main():
    filename = "f:/ptc/x-20-M050.25/Windchill/codebase/out"
    f=open(filename,'r')
    s=f.readline().rstrip()
    while s:
        os.rename("f:/ptc/x-20-M050.25/Windchill/codebase/" + s, "f:/ptc/x-20-M050.25/Windchill/codebase/"+s+"wait")
	s=f.readline().rstrip()

if __name__ == "__main__":
    main()
