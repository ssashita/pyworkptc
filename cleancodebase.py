import zipfile
import sys
import os


def getJarClasses(jar_file):
    """prints out .class files from jar_file"""
    lst = []
    zf = zipfile.ZipFile(jar_file, 'r')
    try:
        lst = zf.infolist()
        for zi in lst:
            fn = zi.filename
            #if fn.endswith('.class'):
            #    print(fn)
    finally:
        zf.close()
    return [zi.filename for zi in lst if zi.filename.endswith('.class')]


if __name__=="__main__":
    #Usage - python cleancodebase.py p:/Windchill/srclib/wnc/Foundation.jar  p:/Windchill
    if len(sys.argv) > 2:
        jarpath = sys.argv[1]
        wchome=os.path.abspath(os.path.join(sys.argv[2],'codebase')).replace('\\','/')
        print jarpath, wchome
        lst = getJarClasses(jarpath)
        if len(lst) > 0:
            for f in lst:
                fullpath = os.path.abspath(os.path.join(wchome, f))
                fullpath = fullpath.replace('\\','/')
                if os.path.isfile(fullpath):
                    print fullpath
                    os.remove(fullpath)
                
            
