import re
import datetime
import urllib.request
from timeformat import TIMEFORMAT

req = urllib.request.urlopen("http://localhost/sse?topics=demo")
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

while True:
    now = datetime.datetime.now(JST)
    line = req.readline().decode()
    if line != '\n':
        dt = re.search(r'\[(?P<time>[\w\s\+:\/]+)\]', line).group('time')
        log_dt = datetime.datetime.strptime(dt, TIMEFORMAT)
        print(log_dt, now)
        print(log_dt - now)
