import numpy as np


class Baseline:
    def run(self, input: np.array) -> np.array:
        return np.repeat(np.mean(input), np.size(input))


class BaselineMovMean(Baseline):
    def __init__(self, windowSize: int):
        if windowSize is None or windowSize == 0:
            self.windowSize = 1000
        else:
            self.windowSize = windowSize
        
    def run(self, input: np.array) -> np.array:
        return np.resize(np.convolve(input, np.ones(self.windowSize)/self.windowSize, mode='valid'), np.size(input))
