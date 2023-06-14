import numpy as np

class Event:
    dataRate = 1
    def __init__(self) -> None:
        self.startIndex = 0
        self.endIndex = 0
        self.eventDuration = 0
        self.eventMaxima = 0
        self.eventMaximaIndex = 0
        self.eventDwellTime = 0
        self.event = np.empty
        self.eventRiseTime = 0
        self.eventFallTime = 0
        self.integral = 0

    def _calculateDwellTime(self):
        print(str(self.event) + " : " + str(self.startIndex) +  " : " + str(np.size(self.event,0)))
        dwellStart = self.eventMaximaIndex
        dwellEnd = self.eventMaximaIndex
        while ((self.event[dwellStart]>(self.eventMaxima/2)) and (dwellStart>1)):
            dwellStart -= 1
        while ((self.event[dwellEnd]>(self.eventMaxima/2)) and (dwellEnd < (np.size(self.event,0) - 1))):
            dwellEnd += 1
        self.eventDwellTime = (dwellEnd - dwellStart) * Event.dataRate

    def _calculateRiseFallTime(self):
        self.eventRiseTime = (self.eventMaximaIndex) * Event.dataRate
        self.eventFallTime = (self.endIndex - self.eventMaximaIndex)

    def _calculateIntegral(self):
        self.integral = np.sum(self.event)

    def extractFeatures(self):
        if ((self.startIndex == 0) or (self.endIndex == 0) or (self.eventDuration == 0) or (self.eventMaxima == 0)):
            print(self.startIndex)
            print(self.endIndex)
            print(self.eventDuration)
            print(self.eventMaxima)
            raise Exception("Could not extract event features")
        else:
            self._calculateDwellTime()
            self._calculateRiseFallTime()
            self._calculateIntegral()

    
       
class EventDetect:
    def __init__(self) -> None:
        self.count = 0
        self.peakStart = 0
        self.peakEnd = 0
        self.threshold = 0
        self.eventList = []

    def run(self,input :np.array,threshold : int) -> list:
        data = input[1,:]
        self.peaks = np.zeros(data.shape)
        self.times = np.zeros(data.shape)
        self.threshold = threshold
        while(self.peakStart<(np.size(input,1)-2)):
            if((data[self.peakStart+2] >= self.threshold) and (data[self.peakStart+2]>data[self.peakStart])):
                self.peakEnd = self.peakStart
                while data[self.peakEnd]>0:
                    self.peakEnd += 1
                
                if (self.peakEnd>self.peakStart+2):
                    e = Event()
                    e.event = data[self.peakStart:self.peakEnd]
                    e.startIndex = self.peakStart
                    e.endIndex = self.peakEnd
                    e.eventMaximaIndex = np.argmax(data[self.peakStart:self.peakEnd])
                    e.eventMaxima = data[self.peakStart + e.eventMaximaIndex]
                    e.eventDuration = self.peakEnd - self.peakStart

                    self.peaks[self.peakStart + e.eventMaximaIndex] = e.eventMaxima
                    self.times[self.peakStart:self.peakEnd] = -10


                    self.count += 1
                    self.peakStart = self.peakEnd
                    self.eventList.append(e)
            self.peakStart +=1
        return self.eventList, self.peaks, self.times

                    

