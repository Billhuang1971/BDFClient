import numpy as np


class EEGData(object):
    def __init__(self, data, lenFile, lenBlock, lenWin, labels):
        self.data = data
        self.lenFile = lenFile
        self.lenBlock = lenBlock
        self.updateFrom = 0
        self.updateTo = lenBlock
        self.lenWin = lenWin
        self.fromBlock = 0
        self.toBlock = lenWin
        self.labels = labels
        self.startBlock = 0
        self.case = 0

    def queryRange(self, startWin):
        try:
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
                self.labels = [label for label in self.labels if (label[1] >= readFrom and label[1] < readTo) or (label[2] >= readFrom and label[2] < readTo) or (label[1] < readFrom and label[2] >= readTo)]
                mid = int(readFrom - self.startBlock)
                self.data = self.data[:, mid:]
                self.updateFrom = self.lenBlock - readFrom + self.startBlock
                self.updateTo = self.lenBlock
                startBlock = self.startBlock
                self.startBlock = readFrom
                readFrom = startBlock + self.lenBlock
            else:
                self.case = 3
                self.labels = [label for label in self.labels if (label[1] >= readFrom and label[1] < readTo) or (label[2] >= readFrom and label[2] < readTo) or (label[1] < readFrom and label[2] >= readTo)]
                mid = int(readTo - self.startBlock)
                self.data = self.data[:, :mid]
                self.updateFrom = 0
                self.updateTo = self.startBlock - readFrom
                readTo = self.startBlock
                self.startBlock = readFrom
        except Exception as e:
            print("queryRange", e)
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
                self.labels.extend(labels)
            elif self.case == 3:
                labels.extend(self.labels)
                self.labels = labels
        except Exception as e:
            print("setData", e)

    def getData(self):
        try:
            data = self.data[:, self.fromBlock: self.toBlock]
            labels = []
            if self.labels is None or len(self.labels) == 0:
                return data, labels
            for label in self.labels:
                if (label[1] >= self.startBlock + self.fromBlock and label[1] < self.startBlock + self.toBlock) or (label[2] >= self.startBlock + self.fromBlock and label[2] < self.startBlock + self.toBlock) or (label[1] < self.startBlock + self.fromBlock and label[2] >= self.startBlock + self.toBlock):
                    labels.append(label)
            return data, labels
        except Exception as e:
            print("getData", e)

    def resetEEGData(self, lenBlock, lenWin, startWin, lenFile):
        self.lenBlock = lenBlock
        self.lenWin = lenWin
        self.lenFile = lenFile
        self.updateFrom = 0
        self.updateTo = lenBlock
        self.case = 1

        if self.lenBlock == self.lenFile or startWin < (lenBlock - lenWin) // 2:
            self.startBlock = 0
        elif startWin + lenWin + (lenBlock - lenWin) // 2 > lenFile:
            self.startBlock = lenFile - lenBlock
        else:
            self.startBlock = startWin - (lenBlock - lenWin) // 2
        self.fromBlock = startWin - self.startBlock
        self.toBlock = self.fromBlock + lenWin
        return self.startBlock, self.startBlock + lenBlock

    def insertSample(self, label):
        idx = 0
        while idx < len(self.labels):
            if label[1] < self.labels[idx][1] or (label[1] == self.labels[idx][1] and label[2] < self.labels[idx][2]):
                break
            idx += 1
        self.labels.insert(idx, label)

    def updateSample(self, label):
        idx = 0
        while idx < len(self.labels):
            if label[0] == self.labels[idx][0] and label[1] == self.labels[idx][1] and label[2] == self.labels[idx][2]:
                self.labels[idx][3] = label[3]
                break
            idx += 1

    def deleteSample(self, label):
        idx = 0
        while idx < len(self.labels):
            if label == self.labels[idx]:
                break
            idx += 1
        self.labels.pop(idx)