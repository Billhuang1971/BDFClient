import numpy as np


class EEGData(object):
    def __init__(self):
        self.startBlock = 0
        self.lenBlock = 0
        self.data = np.array([])
        self.lenFile = 0
        self.updateFrom = 0
        self.updateTo = 0
        self.case = 0
        self.fromBlock = 0
        self.toBlock = 0
        self.nSamples = 0
        self.lenWin = 0
        self.labels = []

    def queryRange(self, startWin):
        if startWin >= self.startBlock and startWin + self.lenWin <= self.startBlock + self.lenBlock:
            self.fromBlock = startWin - self.startBlock
            self.toBlock = startWin - self.startBlock + self.lenWin
            self.case = 0
            return [True, None, None]
        if startWin - (self.lenBlock - self.lenWin) // 2 < 0:
            readFrom = 0
            readTo = self.lenBlock
            self.fromBlock = startWin
            self.toBlock = self.fromBlock + self.lenWin
        elif startWin + self.lenWin + (self.lenBlock - self.lenWin) // 2 > self.lenFile:
            readFrom = self.lenFile - self.lenBlock
            readTo = self.lenFile
            self.fromBlock = startWin - (self.lenFile - self.lenBlock)
            self.toBlock = self.fromBlock + self.lenWin
        else:
            readFrom = startWin - (self.lenBlock - self.lenWin) // 2
            readTo = startWin + self.lenWin + (self.lenBlock - self.lenWin) // 2
            self.fromBlock = (self.lenBlock - self.lenWin) // 2
            self.toBlock = self.fromBlock + self.lenWin
        if self.startBlock + self.lenBlock <= readFrom or self.startBlock >= readTo:
            self.startBlock = readFrom
            self.case = 1
            return [False, int(readFrom), int(readTo)]
        if self.startBlock + self.lenBlock <= readTo:
            self.case = 2
            self.labels = [label for label in self.labels if label[2] >= readFrom]
            mid = int(readFrom - self.startBlock)
            self.data = self.data[:, mid:]
            self.updateFrom = self.lenBlock - readFrom + self.startBlock
            self.updateTo = self.lenBlock
            startBlock = self.startBlock
            self.startBlock = readFrom
            readFrom = startBlock + self.lenBlock
        else:
            self.case = 3
            self.labels = [label for label in self.labels if label[2] < readTo]
            mid = int(readTo - self.startBlock)
            self.data = self.data[:, :mid]
            self.updateFrom = 0
            self.updateTo = self.startBlock - readFrom
            readTo = self.startBlock
            self.startBlock = readFrom

        return [False, int(readFrom), int(readTo)]

    def setData(self, EEG, labels):
        try:
            if self.updateFrom == 0 and self.updateTo == self.lenBlock:
                self.data = EEG
            elif self.updateFrom == 0:
                self.data = np.hstack((EEG, self.data))
            else:
                self.data = np.hstack((self.data, EEG))

            if self.case == 1:
                self.labels = labels
            elif self.case == 2:
                if (labels != None and len(labels) > 0):
                    self.labels.extend(labels)
            elif self.case == 3:
                if (labels != None and len(labels) > 0):
                    self.labels = labels.extend(self.labels)
        except Exception as e:
            print("setData", e)


    def getData(self):
        try:
            data = self.data[:, self.fromBlock: self.toBlock]
            labels = []
            for label in self.labels:
                if label[1] < self.startBlock + self.fromBlock and label[2] < self.startBlock + self.fromBlock:
                    continue
                if label[1] >= self.startBlock + self.toBlock:
                    break
                labels.append(label)
            return data, labels
        except Exception as e:
            print("getData", e)

    def initEEGData(self, data, lenFile, lenBlock, nSample, lenWin, labels):
        self.data = data
        self.lenFile = lenFile
        self.lenBlock = lenBlock
        self.nSample = nSample
        self.updateFrom = 0
        self.updateTo = lenBlock
        self.lenWin = lenWin
        self.fromBlock = 0
        self.toBlock = lenWin
        self.labels = labels

    def insertSample(self, label):
        idx = 0
        print(self.labels)
        while idx < len(self.labels):
            if label[1] < self.labels[idx][1] or (label[1] == self.labels[idx][1] and label[2] < self.labels[idx][2]):
                break
            idx += 1
        self.labels.insert(idx, label)
        print(self.labels)
