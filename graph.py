import matplotlib.pyplot as plt
import numpy as np
import os,json

class Result():
    def __init__(self,fileName) -> None:
        self.fileName = fileName
    
    def dump(self):
        with open("./"+self.fileName, "r") as file:
            result = file.readlines()
        return result

    def drawGraph(self):
        data = self.dump()
        for i in range(len(data)) :
            plt.plot(list(range(len(data[i]))),list(map(lambda x: float(x) * 1e+5,data[i])),label = 'data')
        plt.legend()
        plt.show()
Result('result.txt').drawGraph()