import re
import datetime
import urllib.request
from timeformat import TIMEFORMAT

req = urllib.request.urlopen("http://localhost/sse?topics=demo")
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
n = 0
s = 0
buf_size = 2000

# with open('result', 'w') as fp:
while True:
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    line = req.readline().decode()
    if line != '\n':
        dt = re.search(r'\[(?P<time>[\w\s\+:\/]+)\]', line).group('time')
        log_dt = datetime.datetime.strptime(dt, TIMEFORMAT).timestamp()

        if n < buf_size:
            n += 1
            s += now - log_dt
        else:
            n = 0
            print(s / float(buf_size))
            # fp.write("%s\n" % (s / float(buf_size)))
            s = 0
