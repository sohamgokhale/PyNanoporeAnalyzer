"""
File    : nanoporeData
Author  : Soham Gokhale - UoL MSc Individual Project

Description:
------------
The class provides funtions to load ion channel readings from solid-state 
nanopore sensors. Currently supports loading data from Axon Binary Format
(ABF) files. The data and the parameters associated with it are loaded in
corresponding class members.

Attributes
----------
channelCount    :   Number of channels present in data file
channelList     :   List of channels present in data file
adcUnits        :   Units for each channel (if present in header)
samplingFreq    :   Sampling frequency or sampling rate of the recorded data
samplingTime    :   Sampling time or sampling interval of the recorded data
dataLengthSec   :   Length of recording (in seconds)
dataLengthMin   :   Length of recording (in minutes)
timeAxis        :   Time axis values for the data
timeUnits       :   Unit for time axis
channel         :   ndarray containing samples for all channels present in data
_loaded         :   static (class) variable to check if data has been loaded 

Functions
---------
load(filename)              :   Load data from specified file
clear()                     :   Clear loaded data
getChannel(channel_number)  :   Returns np.array of specified channel's data

"""


import numpy as np
import pyabf


class ABF_Data:
    _loaded = False

    def __init__(self, filename:str="",dataChannel:int=0) -> None:
        """ 
        Initialize all attributes to zero. 
        If filename is specified, proceed to load data.
        """
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
        self.dataChannel = dataChannel
        if (filename is not None or filename != ""):
            self.load(filename)

    def getChannel(self):
        channel_number = self.dataChannel
        """ Load Data and Attributes if not loaded. All channels are loaded into 
        channel array"""

        if not ABF_Data._loaded:
            raise Exception(
                "ERROR: Data not loaded. Call load() function to load data.")
        else:
            if (channel_number < self.channelCount) and (channel_number >= 0):
                return self.channel[channel_number]
            else:
                raise IndexError(
                    "Channel Number must be between 0 - "+str(self.channelCount-1))

    def load(self, filename):
        """ Load data from file."""
        if not ABF_Data._loaded:
            if (filename is None or filename == ""):
                ABF_Data._loaded = False
                raise Exception("ERROR: No file name specified!")
            else:
                ABF_Data._loaded = self._loadABF(filename)
        else:
            raise Exception(
                "ERROR: Data already loaded. Call clear() function before trying to load new data.")

    def clear(self):
        """ Clear all loaded data. """
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
        ABF_Data._loaded = False

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
