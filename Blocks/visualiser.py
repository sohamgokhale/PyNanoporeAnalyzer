import matplotlib.pyplot as plt

class Scatterplot:
    def run(self,xAxis,yAxis) -> None:
        plt.scatter(xAxis,yAxis)
        plt.show()