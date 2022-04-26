from pulsesensor import Pulsesensor
import time

p = Pulsesensor()
p.startAsyncBPM()
start_time = time.time()
file = open("data.csv", "w")

try:
    while True:
        current = time.time() - start_time
        bpm = p.BPM
        if bpm > 0:
            file.write("%d,%d\n" % (bpm,current))
        else:
            file.write("0,%d\n" % current)
        time.sleep(1)
except:
    file.close()
    p.stopAsyncBPM()
