#encoding:utf-8

import math
import sys
import re

maxLength = 0
chunksize = 3

dic = dict()
num_en = dict()
punc = dict()
unit = dict()

def loadDicts():
    fpo = open('words.dic','r')
    for line in fpo:
        word = line.strip().decode('utf8')
        dic.setdefault(word,1)
        global maxLength
        maxLength = max(maxLength,len(word))
    fpo.close()

    fpo = open('chars.dic','r')
    for line in fpo:
        char,freq = line.replace('\n','').decode('utf8').split(' ')
        dic.setdefault(char,int(freq))
    fpo.close()

    fpo = open('num_en.dic','r')
    for line in fpo:
        line = line.strip().decode('utf8')
        if len(line) > 1:
            continue
        num_en.setdefault(line,1)
    fpo.close()

    fpo = open('punctuation.dic','r')
    for line in fpo:
        line = line.strip().decode('utf8')
        if len(line) > 1:
            continue
        punc.setdefault(line,1)
    fpo.close()

    fpo = open('units.dic','r')
    for line in fpo:
        line = line.strip().decode('utf8')
        if len(line) > 1:
            continue
        unit.setdefault(line,1)
    fpo.close()

class Chunk:
    def __init__(self,words):
        self.ChunkWords = words

    def ComLength(self):
        self.ant = 0
        self.cnt = 0
        for word in self.ChunkWords:
            self.ant += len(word)
            self.cnt += 1
        return self.ant

    def AverLength(self):
        self.ave = float(self.ant)/float(self.cnt)
        return self.ave

    def ChangeRate(self):
        self.rate = 0.0
        for word in self.ChunkWords:
            self.rate += math.pow(len(word)-self.ave,2)
        return self.rate

    def CharFreq(self):
        self.lns = 0.0
        for word in self.ChunkWords:
            if len(word) == 1:
                self.lns += math.log10(dic[word])
        return self.lns

class CheckChunk:
    def __init__(self,chunks):
        self.chunkset = chunks

    def compare(self):

        maxlen = 0
        llen = list()
        pos = 0
        for chunk in self.chunkset:
            ll = chunk.ComLength()
            llen.append(ll)
            maxlen = max(maxlen,ll)
        for i in xrange(len(llen)):
            if llen[i] < maxlen:
                del self.chunkset[i-pos]
                pos += 1

        lens = len(self.chunkset)
        if lens == 1 :
            return self.chunkset[0]

        avelen = 0
        del llen[:]
        pos = 0
        for chunk in self.chunkset:
            ll = chunk.AverLength()
            llen.append(ll)
            avelen = max(avelen,ll)
        for i in xrange(lens):
            if llen[i] < avelen:
                del self.chunkset[i-pos]
                pos += 1

        lens = len(self.chunkset)
        if lens == 1:
            return self.chunkset[0]

        rate = 0.0
        del llen[:]
        pos = 0
        tmp = 0
        for chunk in self.chunkset:
            ll = chunk.ChangeRate()
            llen.append(ll)
            if tmp == 0:
                rate = ll
                tmp = 1
            else :
                rate = min(rate,ll)
        for i in xrange(lens):
            if llen[i] > rate:
                del self.chunkset[i-pos]
                pos += 1

        lens = len(self.chunkset)
        if lens == 1:
            return self.chunkset[0]

        lnsum = 0
        del llen[:]
        pos = 0
        for chunk in self.chunkset:
            ll = chunk.CharFreq()
            llen.append(ll)
            lnsum = max(lnsum,ll)
        for i in xrange(lens):
            if llen[i] < lnsum:
                del self.chunkset[i-pos]
                pos += 1

        return self.chunkset[0]

class Handle:
    def __init__(self,sentence):
        self.text = sentence
        self.pos = 0
        self.cnt = 0
        self.words = list()
        self.chunkset = list()
        self.result = list()
        self.handle()

    def getChunk(self):
        if self.cnt == chunksize or self.pos > len(self.text)-1 or self.text[self.pos] not in dic.keys():
            ww = list()
            for word in self.words:
                ww.append(word)
            chunk = Chunk(ww)
            self.chunkset.append(chunk)
            return
        index = self.pos
        k = 1
        while k < maxLength+1 :
            word = self.text[index:index+k]
            if word not in dic.keys():
                k += 1
                continue
            self.words.append(word)
            self.pos = index+k
            self.cnt += 1
            self.getChunk()
            self.cnt += -1
            self.pos = index
            del self.words[self.cnt]
            k += 1
            if index+k > len(self.text):
                break

    def handle(self):
        while self.pos < len(self.text):
            if self.text[self.pos] in num_en.keys():
                index = self.pos
                for i in xrange(self.pos,len(self.text),1):
                    if self.text[i] not in num_en.keys():
                        break
                self.pos = i
                if self.text[self.pos] in unit.keys() or self.pos == len(self.text)-1 :
                    self.pos += 1
                self.result.append(self.text[index:self.pos])
                continue

            if self.text[self.pos] in punc.keys():
                self.result.append(self.text[self.pos])
                self.pos += 1
                continue

            del self.chunkset[:]
            self.getChunk()
            chunk = CheckChunk(self.chunkset)
            if not chunk:
                continue
            words = chunk.compare().ChunkWords
	    if not words:
		continue
            self.result.append(words[0])
            self.pos += len(words[0])

class Solve:
    def __init__(self,document):
        self.doc = document
        self.prehandle()

    def prehandle(self):
        fpo = open(self.doc,'r')
        texts = list()

        for line in fpo:
            line = line.strip().decode('utf8')
            texts.append(line)
        fpo.close()

        filename,_ = self.doc.split('.')
        filename += '_result1.utf8'

        for line in texts:
            line = line.replace('\n','')
            words = Handle(line).result
            strs = ''
            for word in words:
                strs += (word+'  ')
            strs += '\n'
            fpw = open(filename,'a')
            fpw.writelines(strs.encode('utf8'))
            fpw.close()
            '''
            for c in stop.keys():
                if c in line:
                    sen = line.split(c)
            for text in line:
                print text
                words = Handle(text).result
                strs = ""
                for word in words:
                    strs += (word+'  ')
                strs += '\n'
                fpw.writelines(strs.encode('utf8'))
            '''

if __name__=="__main__":
    loadDicts()
    Solve(sys.argv[1])
