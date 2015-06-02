# getPartialMSLog.py
# Script for giving the cumulative time spent to deflate Type instances.
# Inputs are the MS log file name and the starting time (in the time  
# format as printed in MS log) from which the calculation should be done
# So, in the Python shell for example we would have  two lines to run 
# this script, as shown , followed by the output from the script:
#
#>>> sys.argv=['', 'MethodServer-1404302030-10188-log4j.log', '2014-05-02 14:44:05,567']
#>>> execfile("D:/sachin/pyworkptc/getPartialMSLog.py")
#2014-05-02 14:44:05.567000
#Total time in ms :76234
#Start of inflation :2014-05-02 14:44:05.566000
#End of inflation :2014-05-02 14:44:16.314000
#Difference :10.748

import os,sys
from datetime import datetime, timedelta
import re

TIMEDELTA = 15
LOGTIMEFORMAT='20%y-%m-%d %H:%M:%S,%f'

if __name__=="__main__":
    mslogname = sys.argv[1]
    starttime = sys.argv[2]
    endtime=None
    etime=None

    if len(sys.argv) >3:
        endtime = sys.argv[3]
        etime = datetime.strptime(endtime+'000', LOGTIMEFORMAT)

    stime=datetime.strptime(starttime+'000', LOGTIMEFORMAT)
    print stime
    
    f=open(mslogname,"r")
    line=f.readline()
    ms =0
    maxTime = stime.min
    minTime = stime.max
    while line:
        words=re.split("\s",line)
        if re.match("^2014.*",line):
            linetime=words[0] + ' ' + words[1]
            ltime = datetime.strptime(linetime+'000',LOGTIMEFORMAT)
            delta= (ltime -stime).total_seconds()
            if etime == None:
                condition = (delta >= 0 and  delta < TIMEDELTA)
            else:
                condition =  (delta >= 0 and (ltime-etime).total_seconds() <= 0)
            if condition:
                if re.match(".*Time to inflate.*",line):
                    #print(words)
                    current_ms = int(words[-3])
                    ms = ms + current_ms
                    if maxTime < ltime:
                        maxTime = ltime
                    if (ltime - timedelta(microseconds=(1000*current_ms))) < minTime:
                        minTime = ltime - timedelta(microseconds=(1000*current_ms))
        line=f.readline()
    f.close()
    print "Total time in ms :" + str(ms)
    print "Start of inflation :" + str(minTime)
    print "End of inflation :" + str(maxTime)
    print "Difference :" + str((maxTime-minTime).total_seconds())
