#!/usr/bin/env python

# Got from Matthieu Brucher, Modified Junjie Qian
# Last edited, 2014

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

colours = ['b', 'g', 'r', 'c', 'm', 'y']

def getPageSize():
  import resource
  f = open("/proc/meminfo")
  mem = f.readline()
  f.close()
  return resource.getpagesize() / (1024 * float(mem[10:-3].strip()))

pagesizepercent = getPageSize()

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
#  import subprocess
#  subprocess.call("jstack %s >> tdump"% pid, shell=True)
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
          d['pcpu'] = 1e6 * ((d['utime'] + d['stime']) - (now['utime'] + now['stime'])) / float((getTime(t) - getTime(now["current_time"])))

        self.data[thread][getTime(t)] = d
        self.data[thread]["now"] = d
#      time.sleep(0.01)

def displayCPU(data, pid):
  """
  Displays and saves the graph
  """
  import pylab
  import numpy
  
  spid = str(pid)

  list1 = []
  dict1 = {}
  c = 0
  threads = data.keys()
  threads.sort()
  for thread in threads:
    d = data[thread]
    keys = d.keys()
    keys.remove("now")
    keys.sort()
    mykeys = numpy.array(keys)/1e6
    mykeys -= mykeys[0]
#    if c > 5:
#      c = 0
 
    list1.append(sum([d[key]['pcpu'] for key in keys[2:]]))
    dict1[str(thread)] = list1[-1]
#    pylab.plot(mykeys[2:], [d[key]['pcpu'] for key in keys[2:]], colours[c], label = thread)
#    c = c+1
#    if spid == thread:
#      pylab.plot(mykeys[2:], [d[key]['pmem'] for key in keys[2:]], 'k', label = 'MEM')

#  pylab.ylim([-5, 105])
#  pylab.legend(loc=6)
  
#  pylab.savefig('%d.svg' % pid)
#  pylab.savefig('%d.png' % pid)
#  pylab.close()
  total = sum(list1)
  list2 = []
  base = 0.0
  for i in range(len(list1)):
    base = list1[i]
    if list1[i] > 0.0:
      list2.append(base/total)
  for item in dict1:
    base = dict1[item]
    if dict1[item] > 0.0:
      dict1[item] = float(base/total)
  return dict1
#  print dict1
#  return list2

if __name__ == "__main__":
  import sys
  import os
  import pickle

  if len(sys.argv) < 5:
    sys.exit("USAGE: python proc.py stdin stdout java-pmd java -jar ../dacapo-9.12-rc1-bach.jar pmd")
  
  stdin = open(sys.argv[1])
  stdout = open(sys.argv[2], "w")
  name = sys.argv[3]

  resultfile = open("%s_results"%name, "a")

  process = subprocess.Popen(sys.argv[4:], stdin = stdin, stdout = stdout)
  import subprocess
  subprocess.call("jstack %s >> %s_tdump"% (process.pid, name), shell=True)
 
  thread = MonitorThread(process.pid)
  thread.start()

  process.wait()

  thread.process = False
  thread.join()
  
  f = open('%d.data' % process.pid, 'w')
  pickle.dump(thread.data, f)

  resultdict = displayCPU(thread.data, process.pid)
  resultfile.write(name+"==")
  for element in resultdict:
    resultfile.write(str(element) + ":" + str(resultdict[element]) + ",")
  resultfile.write("\n")

'''
  resultlist = displayCPU(thread.data, process.pid)
  resultfile.write(name+"==")
  for element in resultlist:
    resultfile.write(str(element)+',')
  resultfile.write("\n")
  resultfile.close()
'''
