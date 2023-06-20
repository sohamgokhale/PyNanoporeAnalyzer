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
class EventCollect

Description:
------------
Contains class EventCollect used as container for storing data associated
with translocation event detected within EventDetect block. The class also
stores data related to events and unpacks the events into various useful 
arrays. The __init__ function is used for setup and configuration and the
unpack() function for calculating event features.

"""


class EventCollector:
    def __init__(self) -> None:
        self.eventList = []
        self.peaks = []
        self.times = []
        self.dwellTimes = []
        self.Amplitudes = []
        self.RiseTimes = []
        self.FallTimes = []
        self.Integrals = []
        self.eventCount = 0

    def unpack(self) -> None:
        for event in self.eventList:
            event.extractFeatures()
            self.dwellTimes.append(event.eventDwellTime)
            self.Amplitudes.append(event.eventMaxima)
            self.RiseTimes.append(event.eventRiseTime)
            self.FallTimes.append(event.eventFallTime)
            self.Integrals.append(event.integral)


"""
class EventDetect

Description:
------------
Contains class EventDetect used for translocation event detection within
signal. The __init__ function is used for setup and configuration and the
run() function for execution. The class returns 'EventCollector' object.

"""


class EventDetect:

    """ Initialize object fields"""

    def __init__(self, samplingTime, _threshold) -> None:
        self._count = 0
        self._peakStart = 0
        self._peakEnd = 0
        self._eventList = []
        if _threshold is None:
            self._threshold = 0
        else:
            self._threshold = _threshold
        self._samplingTime = samplingTime

    """ Run Method to detect events within signal array passed """

    def run(self, input: np.array) -> EventCollector:

        iterator = 0                            # Start Iterator at zero
        # Create Empty arrays for storing
        self._peaks = np.zeros(input.shape)
        self._times = np.zeros(input.shape)      # Event Peaks and Event Times
        ec = EventCollector()                   # Initialise EventCollector

        # iterate through input
        while (iterator < input.size):

            # Collect Event if Amplitude crosses threshold
            if (input[iterator] >= self._threshold):

                self._peakStart = iterator
                self._peakEnd = iterator

                # backtrack to start of event
                while input[self._peakStart] > 0:
                    self._peakStart -= 1

                # move forward to find end of event
                while input[self._peakEnd] > 0:
                    self._peakEnd += 1

                # collect various event details
                if (self._peakEnd > iterator):

                    e = Event(self._samplingTime)
                    e._samplingTime = self._samplingTime
                    e.event = input[self._peakStart:self._peakEnd]
                    e.startIndex = self._peakStart
                    e.endIndex = self._peakEnd

                    e.eventMaximaIndex = np.argmax(
                        input[self._peakStart:self._peakEnd])
                    
                    e.eventMaxima = input[self._peakStart + e.eventMaximaIndex]
                    e.eventDuration = self._peakEnd - self._peakStart

                    self._peaks[self._peakStart +
                                e.eventMaximaIndex] = e.eventMaxima
                    self._times[self._peakStart:self._peakEnd] = -10

                    self._count += 1

                    # Start detecting new event from end of current Event
                    iterator = self._peakEnd

                    # Append detected event to list
                    self._eventList.append(e)

            iterator += 1
        
        # Collect event details in EventCollector Object
        ec.eventList = self._eventList
        ec.peaks = self._peaks
        ec.times = self._times
        ec.eventCount = self._count
        ec.unpack()
        
        return ec
