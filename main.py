import nanoporeData
import filters
import baselineDetect
import eventDetect
import sigUtils
import matplotlib.pyplot as plt

def setup():
    source = nanoporeData.nanoporeData("Data_interim/Dimer_samples_-300mV.abf")
    Filter = filters.ButterworthLPF(4, 16000, source.samplingFreq)
    Baseline = baselineDetect.BaselineMovMean(10000)
    Sub = sigUtils.SubtractAndFlip(flip=True)
    Events = eventDetect.EventDetect(source.samplingTime, 50)
    run(source,Filter,Baseline,Sub,Events)

def run(source,Filter,Baseline,Sub,Events):
    ch = source.getChannel(0)
    filt = Filter.run(ch)
    base = Baseline.run(filt)
    sub = Sub.run(filt,base)
    events = Events.run(sub)

    plt.scatter(events.Amplitudes, events.dwellTimes)
    plt.show()


if __name__ == "__main__":
    setup()