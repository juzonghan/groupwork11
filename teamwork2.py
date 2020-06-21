#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Group 11, CS 212, Lanzhou University"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "ZonghanJu"
__email__ = "juzh18@lzu.edu.cn"
__status__ = "Experimental"

import re
import time
import unicodedata
from subprocess import Popen, PIPE

class log():    #Use class to show log
    def __init__(self,verran):
        """
        For each log you need to provide the range in a certain version you need to check
        Key arguments:
        """
        self.verran = verran    #the range in a certain version
        self.repo = "D:/kernel/linux-stable"    #the data adress
        self.bug_time = {}    #a dic to store the bug and its time
        self.bug_timediff = {}    #a dic to store the bug and its exist time
        self.commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)    #the re to capture every commit
        self.fixes  = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)    #the re to capture every fix
        self.date = re.compile('^Date:\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9]|[1-2]\d|3[0-1]) [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4} (\+|\-)[0-9]{4}$', re.IGNORECASE)
                #the re to capture every date
    def get_data(self,verran):
        """
        to get data from a certain range
        """
        cmd = ["git", "log", "-P", "--no-merges", self.verran]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
        return data

    def time_transfer(self,t):
        """
        change the str into time stamp
        """
        date = time.strptime(t[12:],'%b %d %H:%M:%S %Y %z')
        timeStamp = int(time.mktime(date))
        #print (timeStamp)
        return (timeStamp)

    def get_bug_time(self):
        """
        to get bugs and its related time
        """
        sum1 = 0
        for line in self.get_data(self.verran).split("\n"):
            if(self.date.match(line)):
                cur_date = line
            if(self.fixes.match(line)):
                sum1 += 1
                self.bug_time.update({sum1:[line[11:18],self.time_transfer(cur_date)]})
        print("There are total ",sum1," bugs!", end="\n")
        return self.bug_time

    def timediff(self,a,b):
        """
        minus of two time stamp
        """
        S_per_H = 3600
        H_per_D = 24
        second = a-b
        day = second // (S_per_H*H_per_D)
        return day

    def get_commit(self):
        """
        Get the time length of a bug
        """
        bug_time = self.get_bug_time()
        sign = 0
        sum1 = 0
        for line in self.get_data(self.verran).split('\n'):
             #here I define a sign to note whether the date should be preserved
            if(re.match(self.commit,line)):
                for i in bug_time.keys():
                    if line[7:14] == bug_time[i][0]:
                        sign = 1
                        n = i
            if(re.match(self.date,line)) and (sign == 1):
                sign = 0
                sum1 += 1
                time_exist = self.timediff(bug_time[n][1],self.time_transfer(line))
                self.bug_timediff.update({sum1: time_exist})
        return self.bug_timediff    


def main():
    b = log("v4.1..head").get_commit()
    print(b)


if __name__ == "__main__":
    main() 
          
            
       

