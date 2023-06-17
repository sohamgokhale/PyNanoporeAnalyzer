"""
File    : baselineDetect
Author  : Soham Gokhale - UoL MSc Individual Project

Description:
------------
Contains base class Baseline used for baseline detection that is inherited
by each baseline detection technique class. Each technique has an __init__ 
method for setup and configuration and a run() method for execution.

"""

from abc import ABC, abstractmethod
import numpy as np


class _Baseline(ABC):
    """ Private Abstract class for Basline Detection """
    @abstractmethod
    def run():
        pass


class BaselineMean(_Baseline):
    """ 
    Use mean of whole data as baseline. Fast solution if the data has high
    SNR and a relatively flat baseline. No setup is required, configuration
    is not data dependent.
    """
    def run(self, input: np.array) -> np.array:
        return np.repeat(np.mean(input), np.size(input))


class BaselineMovMean(_Baseline):
    """ 
    Use Moving Window Average filter method to derive baseline of the signal.
    Moving window acts as a smoothing filter with good time domain performance
    characteristics. It works by convolving a rect signal of width 'windowSize'
    and amplitude '1/windowSize' with the input signal.
    """

    """ Setup class variables: Window size Default(1000) """
    def __init__(self, windowSize: int = 1000) -> None:
        self.windowSize = windowSize

    """ Run filter to detect baseline """
    def run(self, input: np.array) -> np.array:
        return np.resize(np.convolve(input, np.ones(self.windowSize)/self.windowSize, mode='valid'), np.size(input))
