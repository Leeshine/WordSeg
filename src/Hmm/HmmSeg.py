#encoding:utf-8
#author:lvshanchun

import sys
import math
import os

class TrainHmm:
    def __init__(self,TrainingFile,TestFile):
        self.train_set = TrainingFile
        self.test_set = TestFile
        self.training()
        self.testing()

    def findIndex(self,i,lens):
        if lens == 1:
            return 'S'
        if i == 0 :
            return 'B'
        if i == lens-1 :
            return 'E'
        return 'M'

    def training(self):
        print 'training ...'
        a = '  '
        fpo = open(self.train_set,'r')
        self.count = dict()
        self.cnt = dict()
        self.words = list()
        strs = ""

        for line in fpo:
            line = line.decode('utf8')
            line = line.replace(' \n','')
            line = line.replace('\n','')
            grap = line.split(a)
            for scen in grap:
                scen = scen.strip()
                lens = len(scen)
                for i in xrange(0,lens):
                    wd = scen[i]
                    if wd not in self.words:
                        self.words.append(wd)
                    st = self.findIndex(i,lens)
                    self.cnt.setdefault(st,0)
                    self.cnt[st] += 1
                    strs += st
                    self.count.setdefault(st,{})
                    self.count[st].setdefault(wd,0)
                    self.count[st][wd] += 1
            strs += ','
        fpo.close()

        ast = dict()
        for i in xrange(len(strs)-2):
            st1 = strs[i]
            st2 = strs[i+1]
            if st1 == ',' or st2 == ',' :
                continue
            ast.setdefault(st1,{})
            ast[st1].setdefault(st2,0)
            ast[st1][st2] += 1

        self.pi = {'B':0.5,'M':0,'E':0,'S':0.5}
        self.matrixA = dict()
        self.matrixB = dict()
        state = ['B','M','E','S']

        for st1 in state:
            self.matrixA.setdefault(st1,{})
            for st2 in state:
                self.matrixA[st1].setdefault(st2,0)

        for st1,item in ast.items():
            for st2 in item.keys():
                self.matrixA[st1][st2] = float(item[st2])/float(self.cnt[st1])

        for st in state:
            self.matrixB.setdefault(st,{})
            for wd in self.words:
                self.matrixB[st].setdefault(wd,1.0/float(self.cnt[st]))

        for st,item in self.count.items():
            for wd in item.keys():
                self.matrixB[st][wd] = float(item[wd])/float(self.cnt[st])

        print 'training completed'

    def testing(self):
        print 'testing ...'
        filename,_ = self.test_set.split('.')
        filename += '_result.utf8'

        fpo = open(self.test_set,'r')
        fpw = open(filename,'w')

        fi = dict()
        state = ['B','E','M','S']

        num = 0
        for eachline in fpo:
            num += 1
            line = eachline.decode('utf8').strip()
            lens = len(line)
            if lens < 1 :
                continue
            wd = line[0]
            for st in state:
                fi.setdefault(1,{})
                if wd not in self.matrixB[st].keys():
                    self.matrixB[st].setdefault(wd,1.0/float(self.cnt[st]))
                fi[1].setdefault(st,self.pi[st]*self.matrixB[st][wd])
            for i in xrange(1,lens):
                wd = line[i]
                fi.setdefault(i+1,{})
                for st1 in state:
                    fi[i+1].setdefault(st1,0)
                    max_num = 0
                    for st2 in state:
                        max_num = max(max_num,fi[i][st2]*self.matrixA[st2][st1])
                    if wd not in self.matrixB[st1].keys():
                        self.matrixB[st1][wd] = 1.0/float(self.cnt[st1])
                    fi[i+1][st1] = max_num*self.matrixB[st1][wd]

            links = list()
            tmp = list()
            for st in state:
                tmp.append([st,fi[lens][st]])
            st1,_ = max(tmp,key=lambda x:x[1])
            links.append(st1)

            for i in xrange(lens,1,-1):
                tmp = list()
                for st in state:
                    tmp.append([st,fi[i-1][st]*self.matrixA[st][st1]])
                st1,sc = max(tmp,key=lambda x:x[1])
                links.append(st1)

            links.reverse()
            strs = ""
            for i in xrange(len(links)):
                st = links[i]
                if st == 'S':
                    strs += (line[i]+'  ')
                    continue
                if st == 'B' or st == 'M':
                    strs += line[i]
                    continue
                if st == 'E':
                    strs += (line[i]+'  ')
            strs += '\n'
            fpw.writelines(strs.encode('utf8'))

        fpo.close()
        fpw.close()
        print 'test completed'

if __name__ == "__main__":
    args = len(sys.argv)
    if(args < 3):
        print "Usage [trainingSet] [testSet] for utf-8"
        sys.exit(1)
    hmm_train = TrainHmm(sys.argv[1],sys.argv[2])
