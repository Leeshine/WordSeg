#encoding:utf-8

import sys

class LoadData:
    def __init__(self,dic,unit):
        self.dicfile = dic
        self.unitfile = unit
        self.readData()

    def readData(self):
        fpd = open(self.dicfile,'r')

        self.dicitem = dict()
        for line in fpd:
            line = line.decode('utf8').strip()
            self.dicitem.setdefault(line,0)

        fpd.close()

        fps = open(self.unitfile,'r')

        self.unititem = dict()
        for line in fps:
            line = line.decode('utf8').strip()
            if line[0] == '#':
                continue
            self.unititem.setdefault(line,0)

        fps.close()
