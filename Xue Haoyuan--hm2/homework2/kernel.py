import re
import time
import unicodedata
from subprocess import Popen, PIPE

class log():
    def __init__(self,verran):      #For each log you need to provide the range in a certain version you need to check.
        self.verran = verran   #The range in a certain version.
        self.repo = "D:/kernel/linux-stable"   
        self.commit_time = {}   #A dictionary to store the commits and it's time.
        self.bug_timediff = {}
        self.commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)    #The re to capture every commit
        self.date = re.compile('^Date:\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9]|[1-2]\d|3[0-1]) [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4} (\+|\-)[0-9]{4}$', re.IGNORECASE)   #The result to capture every date.

    def get_data(self,verran):       #To get data from a certain range
        cmd = ["git", "log", "-P", "--no-merges", self.verran]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
        return data
    
    def time_translate(self,t):        #Change the string into time stamp
        date = time.strptime(t,'%b %d %H:%M:%S %Y %z')
        timeStamp = int(time.mktime(date))
        return (timeStamp)

    def get_commit(self):    #Get bugs and it's related time
        sum = 0
        for line in self.get_data(self.verran).split("\n"):
            if(self.date.match(line)):
                sum += 1
                self.commit_time.update({sum:self.time_translate(line[12:])})
        print("These are total ",sum," commits", end="\n")
        return self.commit_time

def main():
    verran = input("Please input the range of commits you want to check: ")
    result = log(str(verran)).get_commit()
    with open("output.txt","w") as f:
        f.write(str(result))

if __name__ == "__main__":
    main() 
    
    
