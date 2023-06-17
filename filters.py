"""
File    : filter
Author  : Soham Gokhale - UoL MSc Individual Project

Description:
------------
"""

from abc import ABC, abstractmethod
from scipy.signal import butter, filtfilt
import numpy as np


class _Filter(ABC):
    """ Private Abstract class for Basline Detection """
    @abstractmethod
    def run():
        pass


class ButterworthLPF(_Filter):
    """
    Apply N-th order Butterworth Low Pass Filter to remove high frequency
    noise components from the data.
    """

    """ Setup Butterworth filter by calculating coefficients """

    def __init__(self, order: int, cutoff: float, samplingFreq: float) -> None:
        self.order = order
        self.cutoff = cutoff
        self.fs = samplingFreq
        self.b, self.a = butter(order, cutoff, btype='low', fs=samplingFreq)

    """ Apply Butterworth low pass filter to data using calculated coefficients """

    def run(self, input: np.array) -> np.array:
        return filtfilt(self.b, self.a, input)
