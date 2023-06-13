import numpy as np
import pyabf

class NanoporeData:
    def __init__(self,filename=""):
        if(filename is None or filename==""):
            raise Exception("ERROR: No file name specified!")
        else:
            abf = pyabf.ABF(filename)
            print(abf)
            if ((abf.nOperationMode != 3) or (abf.sweepCount>1)):
                raise Exception("ERROR: .abf file must be recorded in Gap Free Mode with single sweep")
            else:
                self.channelCount = abf.channelCount
                self.channelList = abf.channelList
                self.adcUnits = abf.adcUnits
                self.dataRate = abf.dataRate
                self.dataLengthSec = abf.dataLengthSec
                self.dataLengthMin = abf.dataLengthMin
                self.timeAxis = abf.sweepX
                self.timeUnits = abf.sweepUnitsX
                self.channel = np.empty((self.channelCount,self.timeAxis.size))
                for i in self.channelList:
                    abf.setSweep(0,channel= i)
                    self.channel[i] = abf.sweepY
            print(str(filename) + " Loaded Successfully")

    def getChannel(self, channel_number: int):
        if(channel_number<self.channelCount):
            return np.array([self.timeAxis,self.channel[channel_number]])
        else:
            raise IndexError("Channel Number must be between 0 - "+str(self.channelCount-1))
        
    



