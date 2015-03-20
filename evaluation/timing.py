
import atexit
from time import clock

""" From: http://stackoverflow.com/a/1557906 """


def seconds_to_str(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
               [(t*1000,), 1000, 60, 60])


def log(message, elapsed_time):
    line = "="*40
    print
    print line
    print message
    print "Elapsed time:", elapsed_time
    print line
    print


def end_log():
    end = clock()
    elapsed = end - start
    log("Program end.", seconds_to_str(elapsed))


def now():
    return seconds_to_str(clock())

start = clock()
atexit.register(end_log)

