import matplotlib.pyplot as plt
import numpy as np
from dataLoader import DataLoader
from baselineDetect import BaselineMovMean
from eventDetect import Event, EventDetect

data = DataLoader("Data_interim/Linear_DNA_PBS_01.abf").getChannel(0)
mean = BaselineMovMean().run(data,1000)
baselineSub = np.array([data[0,:],data[1,:]-mean])
flipped = np.array([baselineSub[0,:], baselineSub[1,:] * -1])
events, peaks, times = EventDetect().run(flipped,20)

plt.subplot(2,2,1)
plt.plot(data[0,:],flipped[1,:])
plt.plot(data[0,:],peaks)
plt.plot(data[0,:],times)

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

plt.subplot(2,2,2)
plt.scatter(dwellTimes,Amplitudes)

plt.subplot(2,2,3)
plt.scatter(RiseTimes,FallTimes)

plt.subplot(2,2,4)
plt.hist(Integrals)

plt.show()