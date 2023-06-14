import numpy as np

class Event:
    def __init__(self) -> None:
        self.eventStartIndex = 0
        self.eventEndIndex = 0
        self.eventDuration = 0
        self.eventMaxima = 0
        self.eventMaximaIndex = 0
        self.eventDwellTime = 0
        self.event = np.empty
       
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
                
                if (self.peakEnd>self.peakStart):
                    e = Event()
                    e.event = data[self.peakStart:self.peakEnd]
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

                    

