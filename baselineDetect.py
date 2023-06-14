import numpy as np

class Baseline:
    def run(self,input :np.array) -> np.array:
        return np.repeat(np.mean(input[1,:]),np.size(input,1))
    
class BaselineMovMean(Baseline):
    def run(self,input :np.array,windowSize :int) -> np.array:
        return np.resize(np.convolve(input[1,:], np.ones(windowSize)/windowSize, mode='valid'),np.size(input,1))
