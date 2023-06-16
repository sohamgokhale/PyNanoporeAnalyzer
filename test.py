import matplotlib.pyplot as plt
import numpy as np
from nanoporeData import nanoporeData
from baselineDetect import BaselineMovMean
from eventDetect import Event, EventDetect

data = nanoporeData("Data_interim/Linear_DNA_PBS_01.abf")
channel = data.getChannel(0)
mean = BaselineMovMean(1000)
mean1 = mean.run(channel)
baselineSub = channel-mean1
flipped = baselineSub * -1
events, peaks, times = EventDetect(20).run(flipped)

plt.subplot(3,2,1)
plt.plot(data.timeAxis,flipped)
plt.plot(data.timeAxis,peaks)
plt.plot(data.timeAxis,times)

fourier = np.fft.rfft(flipped)
freq = np.fft.rfftfreq(flipped.size,d=data.samplingTime)
fft_mag = abs(fourier) / np.size(channel,0)

plt.subplot(3,2,2)
plt.plot(freq,fft_mag)


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

plt.subplot(3,2,3)
plt.scatter(dwellTimes,Amplitudes)

plt.subplot(3,2,4)
plt.scatter(RiseTimes,FallTimes)

plt.subplot(3,2,5)
plt.hist(Integrals)

plt.show()