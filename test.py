import matplotlib.pyplot as plt
import numpy as np
from dataLoader import DataLoader
from baselineDetect import BaselineMovMean
from eventDetect import Event, EventDetect

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')

data = DataLoader("sample.abf").getChannel(0)
mean = BaselineMovMean().run(data,1000)
ax1.plot(data[0,:],data[1,:])
ax1.plot(data[0,:],mean)
baselineSub = np.array([data[0,:],data[1,:]-mean])
flipped = np.array([baselineSub[0,:], baselineSub[1,:] * -1])
events, peaks, times = EventDetect().run(flipped,20)
ax2.plot(data[0,:],flipped[1,:])
ax2.plot(data[0,:],peaks)
ax2.plot(data[0,:],times)
plt.show()