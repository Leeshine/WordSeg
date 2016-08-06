#encoding:utf-8
import sys
import re

from load import LoadData

class mmSeg:
    def __init__(self,document,dic,unit):
        self.doc = document
        self.dicitem = dic
        self.unititem = unit
        self.num = [u'○',u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十']
        self.maxLen = 10#最大匹配长度
        self.readData()
        self.handle()

    def readData(self):
        fpo = open(self.doc,'r')

        self.sentence = list()
        for line in fpo:
            line = line.decode('utf8').strip()
            self.sentence.append(line)

        fpo.close()

    def simple_mmseg(self,sen):#正向最大匹配
        result = list()
        lens = len(sen)
        pattern1 = re.compile(r'\d+$')
        j = 0
        while j < lens :
            match = False
            k = min(self.maxLen,lens-j)
            while k > 0 :
                words = sen[j:j+k]
                if words[0] in self.num:
                    for i in xrange(len(words)):
                        if words[i] not in self.num:
                            break
                    k = i
                    if words[i] in self.unititem.keys() or j+i == lens-1 :
                        k += 1
                    words = sen[j:j+k]
                    result.append(words)
                    match = True
                    break
                if words in self.dicitem.keys():
                    result.append(words)
                    match = True
                    break
                if pattern1.match(words):
                    if j+k < lens and sen[j+k] in self.unititem.keys():
                        k += 1
                    words = sen[j:j+k]
                    result.append(words)
                    match = True
                    break
                k -= 1
            if not match:
                k = 1
                result.append(sen[j])
            j += k

        return result

    def handle(self):
        filename,_ = self.doc.split('.')
        filename += '_result.utf8'
        fpw = open(filename,'w')
        for sen in self.sentence:
            res = self.simple_mmseg(sen)
            strs = ""
            for words in res:
                strs += (words+'  ')
            strs += '\n'
            fpw.writelines(strs.encode('utf8'))
        fpw.close()

if __name__=="__main__":
    data = LoadData('words.dic','units.dic')
    dic = data.dicitem
    unit = data.unititem
    mmseg = mmSeg(sys.argv[1],dic,unit)
