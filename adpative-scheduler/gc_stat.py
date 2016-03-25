#!/usr/bin/python

import string
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def helper(filename):
  fp = open(filename, 'r')
  ratiolist = []
  resultlist = []
  stoplist = []
  runlist = []
  res_stop = []
  res_run = []
  gctime_list = []
  gctime = 0.000
  gclist = []
  gc = 0
  flag = 0 # default flag: pass the warmup, calculate at the final run
  efficiency = []
  efficiency_run = []
  for line in fp:
#    if line.find("completed warmup 39 in ") >= 0: # passed all 39 warmup
#      flag = 1
    if flag == 0:
      if line.find("->") >= 0: # GC happens
        word = line.split("K->")
        prev = word[0].split(' ')[-1]
        past = word[1].split('K')[0]
        try:
          ratio = float(float(past)/float(prev))
        except:
          pass
        efficiency.append(ratio)
        word2 = line.split()
        gctime += float(word2[-7])
        gc += 1
      elif line.find("threads were stopped:") >=0:  # the stopped time
        word = line.split(" ")
        stop = word[-2]
        stoplist.append(float(stop))
      elif line.find("Application time: ") >=0:   # the running time
        word = line.split(" ")
        run = word[-2]
        runlist.append(float(run))
      elif line.find("%%%") >=0:  # new session begins
        gctime_list.append(gctime)
#        efficiency_run.append(float(sum(efficiency))/float(len(efficiency)))
        res_stop.append(float(sum(stoplist)))
        stoplist = []
        res_run.append(float(sum(runlist)))
        runlist = []
        gctime = 0.00
        gclist.append(gc)
        efficiency = []
        gc = 0
  fp.close()
#  return (float(float(sum(efficiency_run))/float(len(efficiency_run))), )
  return (1, float(sum(gclist)/len(gclist)))

markerlist = ['.', ',', 'o', 'v', '^', '*', '<', '>', 's', 'p', 'x', 'D']
def plot(gcefficiency_default, gcfrequency_default, gcefficiency_fifo, gcfrequency_fifo):
  namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'jython', 'eclipse', 'pmd', \
    'avrora', 'tomcat', 'compiler.compiler', 'compress', 'crypto.signverify', \
    'compiler.sunflow', 'crypto.aes', 'scimark.fft.large', 'xml.validation', 'xml.transform']
  ylist_frequency = []
  ylist_efficiency = []
  xlist = []
  for name in namelist:
    xlist.append(name)
    xlist.append(' ')
    list1 = gcefficiency_default[name]
    list2 = gcfrequency_default[name]
    list3 = gcefficiency_fifo[name]
    list4 = gcfrequency_fifo[name]
    base_efficiency = list1[6]
    base_frequency = list2[6]
    ylist_efficiency.append(float(list3[6])/float(list1[6]))
    ylist_frequency.append(float(list4[6])/float(list2[6]))
    ylist_efficiency.append(0.0)
    ylist_frequency.append(0.0)
  del xlist[-1]
  del ylist_efficiency[-1]
  del ylist_frequency[-1]
  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist_frequency)), ylist_frequency, color="#d3d3d3")
  plt.xticks(range(len(xlist)), xlist, rotation=30)
  plt.xlim([0, len(xlist)])
  plt.ylim([0, 1.2])
  plt.grid()
  plt.xlabel("Benchmarks")
  plt.ylabel("Fraction of GC and mutator in total")
  plt.savefig("gc_efficiency.png", format='png', bbox_inches='tight')
  plt.cla()

def main():
  try:
    script, filename = sys.argv
  except:
    sys.exit("Usage: Filepath needed\n")
  gcefficiency_default = {}
  gcfrequency_default = {}
  gcfrequency_fifo = {}
  gcefficiency_fifo = {}
  visited = {}  # record the visited elements
  default = False # record the logs this folder contains
  fifo = False
  thread = ['1', '2', '4', '8', '16', '32', '48']
  if os.path.isfile(filename):
    print filename, helper(filename)
  else:
    for subdirs, dirs, filelists in os.walk(filename):
      for subdir, _, filelist in os.walk(subdirs):
        if "roundrobin" in subdir: # determine if this folder is for improved
          default = True
          fifo = False
        elif "fifo" in subdir:
          fifo = True
          default = False
        else:
          fifo = False
          default = False
        for filename in filelist:
          f = os.path.join(subdir, filename)
          if not f in visited:
            visited[f] = 1
            (gcefficiency, gcfrequency) = helper(f)
            name = (f.split('_')[-2]).split('/')[-1]
            threadid = f.split('_')[-1]
            index = thread.index(threadid)
            if default == True:
              if not name in gcefficiency_default:
                gcefficiency_default[name] = [0, 0, 0, 0, 0, 0, 0]
                gcfrequency_default[name] = [0, 0, 0, 0, 0, 0, 0]
              gcefficiency_default[name][index] = gcefficiency
              gcfrequency_default[name][index] = gcfrequency
            elif fifo == True:
              if not name in gcefficiency_fifo:
                gcfrequency_fifo[name] = [0, 0, 0, 0, 0, 0, 0]
                gcefficiency_fifo[name] = [0, 0, 0, 0, 0, 0, 0]
              gcefficiency_fifo[name][index] = gcefficiency
              gcfrequency_fifo[name][index] = gcfrequency
  plot(gcefficiency_default, gcfrequency_default, gcefficiency_fifo, gcfrequency_fifo)

if __name__ == "__main__":
  main()