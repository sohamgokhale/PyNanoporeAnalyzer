import matplotlib.pyplot as plt
from dataLoader import DataLoader

data = DataLoader("sample.abf")
ch = data.getChannel(0)
plt.plot(ch[0,:],ch[1,:])
plt.show()