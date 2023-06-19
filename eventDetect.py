"""
File    : eventDetect
Author  : Soham Gokhale - UoL MSc Individual Project
"""

import numpy as np

"""
class Event

Description:
------------
The class acts as container for storing data related to events in the signal.
An object of this class can be used to store one event data in the signal. 

Attributes
----------
startIndex          :   Start Index of event in the signal array
endIndex            :   End Index of event in the signal array
eventDuration       :   Duration of event (Baseline to Baseline)
eventMaxima         :   Peak amplitude of event (from Baseline)
eventMaximaIndex    :   Index of Maxima within event array
eventDwellTime      :   Width of the event at amplitude half of Maxima 
event               :   numpy array containing all data points within the event
eventRiseTime       :   Time from baseline to Event Maxima
eventFallTime       :   Time from Event Maxima back to basline
integral            :   Area under curve of event
_samplingTime       :   Private attribute denoting sampling time (in sec)

Functions
---------
_calculateDwellTime()       :   Calculate dwell time for the event 
_calculateRiseFallTime()    :   Calculate rise time and fall time for the event
_calculateIntegral()        :   Calculate integral of the event
extractFeatures()           :   Validate if event has been populated and calculate
                                all features
"""


class Event:
    _samplingTime = 1

    """ Initialise object with all values zero """

    def __init__(self, samplingTime) -> None:
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
        if samplingTime > 0:
            Event._samplingTime = samplingTime

    """ Calculate Dwell Time of the event from the event array """

    def _calculateDwellTime(self) -> None:
        dwellStart = self.eventMaximaIndex
        dwellEnd = self.eventMaximaIndex

        while ((self.event[dwellStart] > (self.eventMaxima/2))
               and (dwellStart > 1)):
            dwellStart -= 1

        while ((self.event[dwellEnd] > (self.eventMaxima/2))
               and (dwellEnd < (np.size(self.event, 0) - 1))):
            dwellEnd += 1
        self.eventDwellTime = (dwellEnd - dwellStart) * Event._samplingTime

    """ Calculate Rise and Fall Times of the event from the event array """

    def _calculateRiseFallTime(self) -> None:
        self.eventRiseTime = (self.eventMaximaIndex) * Event._samplingTime
        self.eventFallTime = (self.endIndex - self.eventMaximaIndex)

    """ Calculate Integral of the event from the event array """

    def _calculateIntegral(self) -> None:
        self.integral = np.sum(self.event)

    """ Validate id event has been correctly extracted and calculate features """

    def extractFeatures(self) -> None:
        if ((self.startIndex == 0) or (self.endIndex == 0)
                or (self.eventDuration == 0) or (self.eventMaxima == 0)):
            # Raise Exception if Event validation fails
            raise Exception("Could not extract event features")
        else:
            self._calculateDwellTime()
            self._calculateRiseFallTime()
            self._calculateIntegral()


"""
class EventDetect

Description:
------------
Contains class EventDetect used for translocation event detection within
signal. The __init__ function is used for setup and configuration and the
run() function for execution. The class creates a list of 'Events'.

"""

class EventDetect:
    _samplingTime = 1

    def __init__(self, samplingTime, _threshold) -> None:
        self._count = 0
        self._peakStart = 0
        self._peakEnd = 0
        self._eventList = []
        if _threshold is None:
            self._threshold = 0
        else:
            self._threshold = _threshold
        EventDetect._samplingTime = samplingTime

    def run(self, input: np.array) -> list:
        data = input
        iterator = 0
        self._peaks = np.zeros(data.shape)
        self._times = np.zeros(data.shape)

        while (iterator < input.size):
            if (data[iterator] >= self._threshold):

                self._peakStart = iterator
                self._peakEnd = iterator

                while data[self._peakStart] > 0:
                    self._peakStart -= 1

                while data[self._peakEnd] > 0:
                    self._peakEnd += 1

                if (self._peakEnd > iterator):
                    e = Event(EventDetect._samplingTime)
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
                    iterator = self._peakEnd
                    self._eventList.append(e)
            iterator += 1
        e._samplingTime = EventDetect._samplingTime
        print(self._count)
        return self._eventList, self._peaks, self._times
