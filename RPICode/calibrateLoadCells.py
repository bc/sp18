import numpy as np
import time


def collectDataAtZeroLoad(lca, numPointsToCollect=1000, sleepTime=0):
    print("Taring")
    counter = 0
    millivoltMatrix = np.zeros(shape=(numPointsToCollect, 7))
    while counter < numPointsToCollect:
        measured_uncalibrated_millivolt_loads = lca.get_uncalibrated_loads()
        millivoltMatrix[counter] = measured_uncalibrated_millivolt_loads
        counter += 1
        time.sleep(sleepTime)
    offsets = np.mean(millivoltMatrix, axis=0)
    return(offsets)
