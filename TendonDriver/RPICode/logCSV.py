from genericHelperFunctions import *


def loads_to_logCSVline(logFile, loads):
    loadCellCSVLine = ",".join([str(x) for x in loads]) + "\n"
    loadCellWithTime = unixtime_str() + "," + loadCellCSVLine
    logFile.write(loadCellWithTime)


def initialize_loadcell_log():
    logFile = open('/home/pi/Downloads/output_logs/log_' +
                   unixtime_str() + '.txt', 'a')
    commaSeparatedLoadCellCols = ",".join(["l" + str(i) for i in range(7)])
    logFile.write("unixtime," + commaSeparatedLoadCellCols + "\n")
    return(logFile)
