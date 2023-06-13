import matplotlib.pyplot as plt
from nanoporeData import NanoporeData

data = NanoporeData("sample.abf")
ch = data.getChannel(0)
plt.plot(ch[0,:],ch[1,:])
plt.show()