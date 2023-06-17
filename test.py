import matplotlib.pyplot as plt
import numpy as np
from nanoporeData import nanoporeData
from baselineDetect import BaselineMovMean
from eventDetect import Event, EventDetect
from filters import ButterworthLPF

data = nanoporeData("Data_interim/Dimer_samples_-300mV.abf")
channel = data.getChannel(0)
filt = ButterworthLPF(4, 16000, data.samplingFreq)
filtered = filt.run(channel)
mean = BaselineMovMean(10000)
mean1 = mean.run(filtered)
baselineSub = filtered-mean1
flipped = baselineSub * -1
eventDetect = EventDetect(data.samplingTime, 50)
events, peaks, times = eventDetect.run(flipped)
print(len(events))

print("Calculating FFT of RAW")
fourier_raw = np.fft.rfft(channel)
freq_raw = np.fft.rfftfreq(channel.size, d=data.samplingTime)
fft_mag_raw = abs(fourier_raw) / np.size(channel, 0)

print("Calculating FFT of Filtered")
fourier = np.fft.rfft(filtered)
freq = np.fft.rfftfreq(filtered.size, d=data.samplingTime)
fft_mag = abs(fourier) / np.size(channel, 0)

print("Calculating FFT of Flipped")
fourier_flip = np.fft.rfft(flipped)
freq_flip = np.fft.rfftfreq(flipped.size, d=data.samplingTime)
fft_mag_flip = abs(fourier) / np.size(channel, 0)

dwellTimes = []
Amplitudes = []
RiseTimes = []
FallTimes = []
Integrals = []
for event in events:
    event.extractFeatures()
    dwellTimes.append(event.eventDwellTime)
    Amplitudes.append(event.eventMaxima)
    RiseTimes.append(event.eventRiseTime)
    FallTimes.append(event.eventFallTime)
    Integrals.append(event.integral)


"""
FUCK MATPLOTLIB
"""