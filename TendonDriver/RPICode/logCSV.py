from genericHelperFunctions import *


def vector_to_string_csv(list_of_numbers):
    return ",".join([str(x) for x in list_of_numbers])


def loads_to_logCSVline(logFile, loads, references, commands):
    measurement_csv = vector_to_string_csv(loads)
    reference_csv = vector_to_string_csv(references)
    commands_csv = vector_to_string_csv(commands)
    now = unixtime_str() + ","
    logFile.write(now + measurement_csv + reference_csv + commands_csv + "\n")


def to_csv(list_of_strings):
    return ",".join(list_of_strings)


def prepend_muscle_numbers(prefix, n_muscles):
    return [prefix + str(i) for i in range(n_muscles)]


def initialize_loadcell_log():
    logFile = open('/home/pi/Downloads/output_logs/log_' +
                   unixtime_str() + '.txt', 'a')
    measured = to_csv(prepend_muscle_numbers("measured_M", 7))
    reference = to_csv(prepend_muscle_numbers("reference_M", 7))
    command = to_csv(prepend_muscle_numbers("command_M", 7))
    logFile.write("unixtime," + measured + "," +
                  reference + "," + command + "\n")
    return(logFile)
