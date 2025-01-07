import numpy as np


class EEGData(object):
    def __init__(self):
        self.startBlock = 0
        self.lenBlock = None
        self.data = np.array([])
        self.lenFile = None

        self.channels = None
        self.index_channels = None
        self.montages = {}

    def setMontages(self, montages):
        self.montages = montages

    def queryRange(self, startWin, lenWin):
        if startWin >= self.startBlock and startWin + lenWin <= self.startBlock + self.lenBlock:
            fromBlock = startWin - self.startBlock
            toBlock = startWin - self.startBlock + lenWin
            return [True, None, None, int(fromBlock), int(toBlock), None, None, 0]
        if startWin - (self.lenBlock - lenWin) / 2 < 0:
            readFrom = 0
            readTo = self.lenBlock
            fromBlock = startWin
            toBlock = fromBlock + lenWin
        elif startWin + lenWin + (self.lenBlock - lenWin) / 2 > self.lenFile:
            readFrom = self.lenFile - self.lenBlock
            readTo = self.lenFile
            fromBlock = startWin - (self.lenFile - self.lenBlock)
            toBlock = fromBlock + lenWin
        else:
            readFrom = startWin - (self.lenBlock - lenWin) / 2
            readTo = startWin + lenWin + (self.lenBlock - lenWin) / 2
            fromBlock = (self.lenBlock - lenWin) / 2
            toBlock = fromBlock + lenWin
        if self.startBlock + self.lenBlock <= readFrom or self.startBlock >= readTo:
            self.startBlock = readFrom
            return [False, int(readFrom), int(readTo), int(fromBlock), int(toBlock), 0, int(self.lenBlock), 1]
        if self.startBlock + self.lenBlock < readTo:
            mid = int(readFrom - self.startBlock)
            self.data = self.data[:, mid:]
            updateFrom = self.lenBlock - readFrom + self.startBlock
            updateTo = self.lenBlock
            startBlock = self.startBlock
            self.startBlock = readFrom
            readFrom = startBlock + self.lenBlock
            case = 2
        else:
            mid = int(readTo - self.startBlock)
            self.data = self.data[:, :mid]
            updateFrom = 0
            updateTo = self.startBlock - readFrom
            readTo = self.startBlock
            self.startBlock = readFrom
            case = 3
        return [False, int(readFrom), int(readTo), int(fromBlock), int(toBlock), int(updateFrom), int(updateTo), case]

    def setData(self, EEG, from_time, to_time):
        if from_time == 0 and to_time == self.lenBlock:
            self.data = EEG
        elif from_time == 0:
            self.data = np.hstack((EEG, self.data))
        else:
            self.data = np.hstack((self.data, EEG))

    def getData(self, from_time, to_time):
        data = self.data[:, from_time: to_time]
        return data

    def initEEGData(self, lenFile, lenBlock):
        self.data = np.array([])
        self.lenFile = lenFile
        self.lenBlock = lenBlock