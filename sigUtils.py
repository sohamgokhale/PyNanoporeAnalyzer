import numpy as np

class SubtractAndFlip:
    def __init__(self,flip :bool = True) -> None:
        self._flip = flip

    def run(self, input1 :np.array, input2 :np.array) -> np.array:
        self.subtracted = input1-input2
        if(self._flip): 
            self.subtracted *= -1
        return self.subtracted
    
class sigFFT:
    def __init__(self, samplingTime) -> None:
        self.samplingTime = samplingTime

    def run(self, input :np.array) -> np.array:
        fourier = np.fft.rfft(input)
        freq = np.fft.rfftfreq(input.size, d=self.samplingTime)
        fft_mag = abs(fourier) / np.size(input, 0)
        return fft_mag, freq