import re

def get_seconds(time_str):
    time_str = str(time_str)
    pattern = "^(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9]$"
    if(re.match(pattern, time_str)):
        hh, mm, ss = time_str.split(':')
        res = int(hh) * 3600 + int(mm) * 60 + int(ss)
        return res
    else:
        dd, tt = time_str.split(" days, ")
        hh, mm, ss = tt.split(':')
        res = int(dd) * 86400 + int(hh) * 3600 + int(mm) * 60 + int(ss)
        return res
