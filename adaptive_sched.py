#!/usr/bin/env python

# adaptive_sched.py

import subprocess
import threading
import datetime

names = [("pid", int),
         ("comm", str),
         ("state", str),
         ("ppid", int),
         ("pgrp", int),
         ("session", int),
         ("tty_nr", int),
         ("tpgid", int),
         ("flags", int),
         ("minflt", int),
         ("cminflt", int),
         ("majflt", int),
         ("cmajflt", int),
         ("utime", int),
         ("stime", int),
         ("cutime", int),
         ("cstime", int),
         ("priority", int),
         ("nice", int),
         ("0", int),
         ("itrealvalue", int),
         ("starttime", int),
         ("vsize", int),
         ("rss", int),
         ("rlim", int),
         ("startcode", int),
         ("endcode", int),
         ("startstack", int),
         ("kstkesp", int),
         ("kstkeip", int),
         ("signal", int),
         ("blocked", int),
         ("sigignore", int),
         ("sigcatch", int),
         ("wchan", int),
         ("nswap", int),
         ("cnswap", int),
         ("exit_signal", int),
         ("processor", int),]

def collectData(pid, task):
  """
  Collect process list
  """
  f1 = open("/proc/%d/task/%s/stat"%(pid,task))
  f2 = open("/proc/%d/task/%s/statm"%(pid,task))
  t = datetime.datetime.now()
  stat = f1.readline().split()
  mem = f2.readline().split()
  d = dict([(name[0], name[1](el)) for (name, el) in zip(names, stat)])
  d["pmem"] = 100 * float(mem[1]) * pagesizepercent
  return t, d

def getTime(key):
  """
  Returns the time in microseconds
  """
  return (((key.weekday() * 24 + key.hour) * 60 + key.minute) * 60 + key.second) * 1000000 + key.microsecond
  
class MonitorThread(threading.Thread):
  """
  The monitor thread saves the process info every 5 seconds
  """
  def __init__(self, pid):
    import collections

    self.pid = pid
    threading.Thread.__init__(self)
    self.data = collections.defaultdict(dict)
    self.process = True
    
  def run(self):
    import os
    import time

    curr = time.time()
    while self.process and time.time() - curr < 0.1:
      try:
        threads = os.listdir("/proc/%d/task/" % self.pid)
      except:
        continue
      for thread in threads:
        try:
          t, d = collectData(self.pid, thread)
        except:
          continue
        d["current_time"] = t
        if "now" in self.data[thread]:
          now = self.data[thread]["now"]
          d['pcpu'] = 1e6 * ((d['utime'] + d['stime']) - (now['utime'] + now['stime'])) / \
          float((getTime(t) - getTime(now["current_time"])))
        self.data[thread][getTime(t)] = d
        self.data[thread]["now"] = d

    import numpy
    list1 = []
    for thread in self.data.keys():
      d = data[thread]
      keys = d.keys()
      keys.remove("now")
      keys.sort()
      mykeys = numpy.array(keys)/1e6
      mykeys -= mykeys[0] 
      list1.append(sum([d[key]['pcpu'] for key in keys[2:]]))
    total = sum(list1)
    fifo = True
    for i in range(len(list1)):
      if list1[i] > 0.0 and list1[i]/total>0.5:
        fifo = False
        break;
    if fifo:
      subprocess.call(("sudo chrt -f 99 %d"%self.pid).split())

if __name__ == "__main__":
  import sys
  import os
  import pickle

  if len(sys.argv) < 5:
    sys.exit("USAGE: python %s stdin stdout java -jar ../dacapo-9.12-rc1-bach.jar pmd"%sys.argv[0])
  
  stdin = open(sys.argv[1])
  stdout = open("/tmp/stdout", "w")
  # name = sys.argv[3]

  process = subprocess.Popen(sys.argv[4:], stdin = stdin, stdout = stdout)
  #import subprocess
  #subprocess.call("jstack %s >> %s_tdump"% (process.pid, name), shell=True)
 
  thread = MonitorThread(process.pid)
  thread.start()

  process.wait()

  thread.process = False
  thread.join()