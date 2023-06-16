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
        dwellStart = self.eventMaximaIndex
        dwellEnd = self.eventMaximaIndex
        while ((self.event[dwellStart] > (self.eventMaxima/2)) and (dwellStart > 1)):
            dwellStart -= 1
        while ((self.event[dwellEnd] > (self.eventMaxima/2)) and (dwellEnd < (np.size(self.event, 0) - 1))):
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
    def __init__(self, _threshold) -> None:
        self._count = 0
        self._peakStart = 0
        self._peakEnd = 0
        self._eventList = []
        if _threshold is None:
            self._threshold = 0
        else:
            self._threshold = _threshold

    def run(self, input: np.array) -> list:
        data = input
        self._peaks = np.zeros(data.shape)
        self._times = np.zeros(data.shape)
        while (self._peakStart < (np.size(input)-2)):
            if ((data[self._peakStart+2] >= self._threshold) and
                    (data[self._peakStart+2] > data[self._peakStart])):
                self._peakEnd = self._peakStart
                while data[self._peakEnd] > 0:
                    self._peakEnd += 1

                if (self._peakEnd > self._peakStart+2):
                    e = Event()
                    e.event = data[self._peakStart:self._peakEnd]
                    e.startIndex = self._peakStart
                    e.endIndex = self._peakEnd
                    e.eventMaximaIndex = np.argmax(
                        data[self._peakStart:self._peakEnd])
                    e.eventMaxima = data[self._peakStart + e.eventMaximaIndex]
                    e.eventDuration = self._peakEnd - self._peakStart

                    self._peaks[self._peakStart +
                                e.eventMaximaIndex] = e.eventMaxima
                    self._times[self._peakStart:self._peakEnd] = -10

                    self._count += 1
                    self._peakStart = self._peakEnd
                    self._eventList.append(e)
            self._peakStart += 1
        return self._eventList, self._peaks, self._times
