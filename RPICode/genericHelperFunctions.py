import time


def current_milli_time():
    return(int(round(time.time() * 1000)))


def unixtime_str():
    return(str(current_milli_time()))
# via
# https://stackoverflow.com/questions/11122291/python-find-char-in-string-can-i-get-all-indexes


def find(string_of_interest, character):
    return [i for i, ltr in enumerate(string_of_interest) if ltr == character]
