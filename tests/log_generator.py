"""
::1 - - [06/Sep/2018:04:24:17 +0000] "GET /favicon.ico HTTP/1.1" 404 209
"""

import datetime
import argparse
from timeformat import TIMEFORMAT

FORMAT = '::1 - - [{time}] "GET /favicon.ico HTTP/1.1" 404 209'

def generate(log_path=None, times=1, interval=1000, forever=False):
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    while True:
        fp = None
        if log_path:
            fp = open(log_path, 'a')

        for i in range(times):
            t = datetime.datetime.now(JST)
            print(FORMAT.format(time=t.strftime(TIMEFORMAT)), file=fp)

        if fp:
            fp.close()
        if not forever:
            break

if __name__ == '__main__':
    generate("busy_access_log", times=100000)
