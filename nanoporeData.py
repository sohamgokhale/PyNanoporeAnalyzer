import numpy as np
import pyabf


class nanoporeData:
    _loaded = False

    def __init__(self, filename=""):
        self.channelCount = 0
        self.channelList = 0
        self.adcUnits = []
        self.samplingFreq = 0
        self.samplingTime = 0
        self.dataLengthSec = 0
        self.dataLengthMin = 0
        self.timeAxis = np.empty((1,))
        self.timeUnits = 0
        self.channel = np.empty((1,))
        if (filename is not None or filename != ""):
            self.load(filename)

    def getChannel(self, channel_number: int):
        if (channel_number < self.channelCount) and (channel_number >= 0):
            return self.channel[channel_number]
        else:
            raise IndexError(
                "Channel Number must be between 0 - "+str(self.channelCount-1))

    def load(self, filename):
        if (filename is None or filename == ""):
            _loaded = False
            raise Exception("ERROR: No file name specified!")
        else:
            _loaded = self._loadABF(filename)

    def _loadABF(self, filename) -> bool:
        abf = pyabf.ABF(filename)
        try:
            print(abf)
            if ((abf.nOperationMode != 3) or (abf.sweepCount > 1)):
                raise Exception(
                    "ERROR: .abf file must be recorded in Gap Free Mode with single sweep")
            else:
                self.channelCount = abf.channelCount
                self.channelList = abf.channelList
                self.adcUnits = abf.adcUnits
                self.samplingFreq = abf.dataRate
                self.samplingTime = 1/(abf.dataRate)
                self.dataLengthSec = abf.dataLengthSec
                self.dataLengthMin = abf.dataLengthMin
                self.timeAxis = abf.sweepX
                self.timeUnits = abf.sweepUnitsX
                self.channel = np.empty(
                    (self.channelCount, self.timeAxis.size))
                for i in self.channelList:
                    abf.setSweep(0, channel=i)
                    self.channel[i] = abf.sweepY
                return True
        except:
            return False
