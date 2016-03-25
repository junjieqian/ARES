#!/usr/bin/env Python
# Total time for which application threads were stopped: 0.0008220 seconds
# Application time: 0.0275980 seconds

# Update 02/15/2014: 40 iterations, first 39 are warmup

import string
import sys
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

colors = ['0.1', '0.25', '0.4', '0.55', '0.7', '0.85', '1']

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
  for line in fp:
#    if line.find("completed warmup 39 in ") >= 0: # passed all 39 warmup
#      flag = 1
    if flag == 0:
      if line.find("->") >= 0: # GC happens
        word = line.split("K->")
#        prev = word[0].split(' ')[-1]
#        past = word[1].split('K')[0]
#        print prev, past, filename
#        ratio = float(float(past)/float(prev))
#        resultlist.append(ratio)
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
        resultlist = []
        res_stop.append(float(sum(stoplist)))
        stoplist = []
        res_run.append(float(sum(runlist)))
        runlist = []
        gctime = 0.00
        gclist.append(gc)
        gc = 0
  fp.close()
  return (float(float(sum(gctime_list))/float(len(gctime_list))), float(float(sum(res_run))/float(len(res_run))), float(sum(gclist)/len(gclist)))

def plot_gc(gcdict_default, mutatordict_default, gcdict_fifo, \
  mutatordict_fifo, gcdict_improved, mutatordict_improved):
  namelist = ['scimark.fft.large', 'eclipse', 'jython', 'h2', 'tomcat', \
        'avrora', 'pmd', 'sunflow', 'xalan', 'lusearch', 'compiler.compiler', 'compiler.sunflow', \
  'compress', 'crypto.aes', 'crypto.signverify', \
  'xml.transform', 'xml.validation']
  ylist_cfs = []
  ylist_fifo = []
  xlist = []
  statlist = []
  minor_ticks = []
  j = 0;
  for name in namelist:
    xlist.append(name)
    minor_ticks.append(j)
    list1 = gcdict_default[name]
    list2 = gcdict_fifo[name]
    base = list1[0]
    for i in range(len(list1)):
      j += 2
      ylist_cfs.append(float(list1[i])/float(base))
      ylist_cfs.append(0.0)
      ylist_fifo.append(0.0)
      ylist_fifo.append(float(list2[i])/float(base))
      statlist.append(float(list1[i])/float(base))
      xlist.append(' ')
      xlist.append(' ')
    ylist_cfs.append(0.0)
    j += 1
    ylist_fifo.append(0.0)
  print len(xlist), len(ylist_fifo)
  fig = plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist_cfs)), ylist_cfs, color="#d3d3d3", edgecolor="k", label="Existing CFS GC Time")
  plt.bar(range(len(ylist_fifo)), ylist_fifo, color="#696969", edgecolor='k', label="FIFO GC Time")
  plt.xticks(range(len(xlist)), xlist, rotation=30, fontsize=12)
  plt.xlim([0, len(xlist)])
  plt.ylim([0,4])
  plt.legend(loc="upper center",fontsize=16,fancybox=True, ncol=2).get_frame().set_alpha(0.5)
  plt.xlabel("Benchmarks running with different numbers of CPU cores (1,2,4,8,16,32,48)", fontsize=16)
  plt.ylabel("GC execution time normalized to run with the CFS scheduler on 1 CPU core", fontsize=16)
  ax = fig.add_subplot(1,1,1)
  ax.set_xticks(minor_ticks, minor=True)
  ax.grid(which='minor', linewidth=0.5, linestyle='-', color='0.75')
  plt.text(0.6,1.03,'5.15  9.43', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
  plt.savefig("gc_scalability_comp.png", bbox_inches='tight')
  plt.cla()
  print float(sum(statlist))/float(len(statlist)), max(statlist), min(statlist)
#  print sorted(statlist)

def plot3(gcdict_default, mutatordict_default, gcdict_fifo, mutatordict_fifo, gcdict_improved, mutatordict_improved):
  namelist = []
  j = -1
  xlist = []
  ylist_gc_default = []  # GC
  ylist_mu_default = []  # mutator
  ylist_gc_fifo = []  # GC
  ylist_mu_fifo = []  # mutator
  ylist_gc_improved = []
  ylist_mu_improved = []
  #namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython']
#  namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython', 'eclipse', 'pmd', \
#  'avrora', 'tomcat', 'compiler.sunflow', 'crypto.aes', 'scimark.fft.large', 'xml.validation', 'xml.transform']
  namelist = ['pmd']
  for name in namelist:
    j += 1
    xlist.append('1')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append('2')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append('4')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append('8')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append('16')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append('32')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append('48')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    list1 = gcdict_default[name]
    list2 = mutatordict_default[name]
    list3 = gcdict_fifo[name]
    list4 = mutatordict_fifo[name]
    list5 = gcdict_improved[name]
    list6 = mutatordict_improved[name]
#    base = list1[0] + list2[0]
    base = 1.0
    for i in range(len(list1)):
      ylist_gc_default.append(float(list1[i])/float(base))
      ylist_mu_default.append(float(list2[i])/float(base))
      ylist_gc_default.append(0.0)
      ylist_mu_default.append(0.0)
      ylist_gc_default.append(0.0)
      ylist_mu_default.append(0.0)

      ylist_gc_fifo.append(0.0)
      ylist_mu_fifo.append(0.0)
      ylist_gc_fifo.append(float(list3[i])/float(base))
      ylist_mu_fifo.append(float(list4[i])/float(base))
      ylist_gc_fifo.append(0.0)
      ylist_mu_fifo.append(0.0)

      ylist_gc_improved.append(0.0)
      ylist_mu_improved.append(0.0)
      ylist_gc_improved.append(0.0)
      ylist_mu_improved.append(0.0)
      ylist_gc_improved.append(float(list5[i])/float(base))
      ylist_mu_improved.append(float(list6[i])/float(base))

    ylist_gc_default.append(0.0)
    ylist_mu_default.append(0.0)
    ylist_gc_fifo.append(0.0)
    ylist_mu_fifo.append(0.0)
  del xlist[-1]
  del ylist_gc_default[-1]
  del ylist_mu_default[-1]
  del ylist_mu_fifo[-1]
  del ylist_gc_fifo[-1]
#  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist_mu_default)), ylist_mu_default, color="#5f9ea0", edgecolor="k", label="Existing Completion Time")
  plt.bar(range(len(ylist_gc_default)), ylist_gc_default, bottom=ylist_mu_default, color='#0000ff', \
    edgecolor="k", label="Existing Pause Time")
  plt.bar(range(len(ylist_mu_fifo)), ylist_mu_fifo, color="#d3d3d3", edgecolor="k", label="FIFO Completion Time")
  plt.bar(range(len(ylist_gc_fifo)), ylist_gc_fifo, bottom=ylist_mu_fifo, color='#696969', edgecolor="k", label="FIFO Pause Time")
#  plt.bar(range(len(ylist_mu_improved)), ylist_mu_improved, color="#d3d3d3", edgecolor="k", hatch='\\', label="Improved Completion Time")
#  plt.bar(range(len(ylist_gc_improved)), ylist_gc_improved, bottom=ylist_mu_improved, color='#696969', edgecolor="k", \
#    hatch='\\', label="Improved Pause Time")
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
#  plt.ylim([0, 1.2])
  plt.legend(loc="upper center", ncol=2, prop={'size':9})
  plt.xlabel("pmd running with different numbers of CPU cores")
  plt.ylabel("Execution time divided into GC and mutator (secs)")
  plt.savefig("gcfraction.png", bbox_inches='tight')
  plt.cla()

def plot4(gcdict_default, mutatordict_default, gcdict_fifo, mutatordict_fifo, gcdict_improved, mutatordict_improved):
  # plot the 48 cores only
  namelist = []
  j = -1
  xlist = []
  ylist_gc_default = []  # GC
  ylist_mu_default = []  # mutator
  ylist_gc_fifo = []  # GC
  ylist_mu_fifo = []  # mutator
  ylist_gc_improved = []
  ylist_mu_improved = []
  #namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython']
  #namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'jython', 'eclipse', 'pmd', \
  #  'avrora', 'tomcat', 'compiler.compiler', 'compress', 'crypto.signverify', \
  #  'compiler.sunflow', 'crypto.aes', 'scimark.fft.large', 'xml.validation', 'xml.transform']
  namelist = ['mpegaudio', 'scimark.fft.large', 'eclipse', 'fop', 'jython', 'h2', 'tomcat', \
        'avrora', 'pmd', 'sunflow', 'xalan', 'lusearch', 'compiler.compiler', 'compiler.sunflow', \
	'compress', 'crypto.aes', 'crypto.signverify', \
	'xml.transform', 'xml.validation']
  temp = []
  for name in namelist:
    j += 1
    xlist.append(' ')
    xlist.append(name)
    xlist.append(' ')
    xlist.append(' ')
    list1 = gcdict_default[name]
    list2 = mutatordict_default[name]
    list3 = gcdict_fifo[name]
    list4 = mutatordict_fifo[name]
    list5 = gcdict_improved[name]
    list6 = mutatordict_improved[name]
    base = list1[-1] + list2[-1]
    for i in range(len(list1)-1, len(list1)):
      ylist_gc_default.append(float(list1[i])/float(base))
      ylist_mu_default.append(float(list2[i])/float(base))
      ylist_gc_default.append(0.0)
      ylist_mu_default.append(0.0)
      ylist_gc_default.append(0.0)
      ylist_mu_default.append(0.0)

      ylist_gc_fifo.append(0.0)
      ylist_mu_fifo.append(0.0)
      ylist_gc_fifo.append(float(list3[i])/float(base))
      ylist_mu_fifo.append(float(list4[i])/float(base))
      ylist_gc_fifo.append(0.0)
      ylist_mu_fifo.append(0.0)

      ylist_gc_improved.append(0.0)
      ylist_mu_improved.append(0.0)
      ylist_gc_improved.append(0.0)
      ylist_mu_improved.append(0.0)
      ylist_gc_improved.append(float(list5[i])/float(base))
      ylist_mu_improved.append(float(list6[i])/float(base))

      print ((float(list5[i])+float(list6[i]))/float(base)), name
      temp.append((float(list5[i])+float(list6[i]))/float(base))

    ylist_gc_default.append(0.0)
    ylist_mu_default.append(0.0)
    ylist_gc_fifo.append(0.0)
    ylist_mu_fifo.append(0.0)
    ylist_gc_improved.append(0.0)
    ylist_mu_improved.append(0.0)
  del xlist[-1]
  del ylist_gc_default[-1]
  del ylist_mu_default[-1]
  del ylist_mu_fifo[-1]
  del ylist_gc_fifo[-1]
  plt.figure(figsize=(25, 10))
  plt.bar(range(len(ylist_mu_default)), ylist_mu_default, color="#5f9ea0", edgecolor="k", label="Existing CFS Completion Time")
  plt.bar(range(len(ylist_gc_default)), ylist_gc_default, bottom=ylist_mu_default, color='#0000ff', \
    edgecolor="k", label="Existing CFS Pause Time")
  plt.bar(range(len(ylist_mu_fifo)), ylist_mu_fifo, color="#d3d3d3", edgecolor="k", label="FIFO Completion Time")
  plt.bar(range(len(ylist_gc_fifo)), ylist_gc_fifo, bottom=ylist_mu_fifo, color='#696969', edgecolor="k", label="FIFO Pause Time")
  plt.bar(range(len(ylist_mu_improved)), ylist_mu_improved, color="#d3d3d3", edgecolor="k", hatch='\\', label="Proposed Scheduler Completion Time")
  plt.bar(range(len(ylist_gc_improved)), ylist_gc_improved, bottom=ylist_mu_improved, color='#696969', edgecolor="k", \
    hatch='\\', label="Proposed Scheduler Pause Time")
  plt.xticks(range(len(xlist)), xlist, rotation=30)
  plt.xlim([0, len(xlist)])
  plt.ylim([0, 1.6])
  plt.grid()
  plt.legend(loc="upper center", ncol=3)
  plt.xlabel("Benchmarks")
  plt.ylabel("Normalized GC and mutator time")
  plt.savefig("cfs_fifo_48only.png", bbox_inches='tight')
  plt.cla()
  print float(sum(temp))/float(len(temp))

def plot2(gcdict_default, mutatordict_default, gcdict_improved, mutatordict_improved):
  namelist = []
  xlist = []
  ylist_gc_default = []  # GC
  ylist_mu_default = []  # mutator
  ylist_gc_improved = []  # GC
  ylist_mu_improved = []  # mutator
#  namelist = ['lusearch', 'xalan', 'sunflow', 'compiler.sunflow', 'xml.validation', 'xml.transform']
#  namelist = ['compiler.compiler', 'compress', 'crypto.signverify', 'mpegaudio']
  # namelist = ['lusearch', 'xalan', 'sunflow', 'pmd', 'avrora', \
  # 'compiler.sunflow', 'crypto.aes', 'xml.validation', 'xml.transform', \
  # 'compiler.compiler', 'compress', 'crypto.signverify']
  namelist = ['h2', 'eclipse', 'tomcat', 'scimark.fft.large', 'jython']
  statlist = []
  minor_ticks = []
  j = 0
  for name in namelist:
    minor_ticks.append(j)
    # xlist.append(name)
    xlist.append(' ')
#    xlist.append('2')
    xlist.append(' ')
#    xlist.append('4')
    xlist.append(' ')
#    xlist.append('8')
    xlist.append(' ')
    xlist.append(name)
#    xlist.append('16')
    xlist.append(' ')
#    xlist.append('32')
    xlist.append(' ')
#    xlist.append('48')
    xlist.append(' ')
    xlist.append(' ')

    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    j+=15

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list1 = gcdict_default[name]
    list2 = mutatordict_default[name]
    list3 = gcdict_improved[name]
    list4 = mutatordict_improved[name]
    base = list1[0] + list2[0]
    for i in range(len(list1)):
      ylist_gc_default.append(float(list1[i])/float(base))
      ylist_mu_default.append(float(list2[i])/float(base))
      ylist_gc_default.append(0.0)
      ylist_mu_default.append(0.0)
      ylist_gc_improved.append(0.0)
      ylist_mu_improved.append(0.0)
      ylist_gc_improved.append(float(list3[i])/float(base))
      ylist_mu_improved.append(float(list4[i])/float(base))
      statlist.append(float(list3[i] + list4[i])/base)
    ylist_gc_default.append(0.0)
    ylist_mu_default.append(0.0)
    ylist_gc_improved.append(0.0)
    ylist_mu_improved.append(0.0)
  del xlist[-1]
  del ylist_gc_default[-1]
  del ylist_mu_default[-1]
  del ylist_mu_improved[-1]
  del ylist_gc_improved[-1]
  fig = plt.figure(figsize=(30, 10))
  plt.bar(range(len(ylist_mu_default)), ylist_mu_default, color="#5f9ea0", edgecolor="k", label="Existing CFS Mutator Time")
  plt.bar(range(len(ylist_gc_default)), ylist_gc_default, bottom=ylist_mu_default, color='#0000ff', edgecolor="k", label="Existing CFS GC Time")
  plt.bar(range(len(ylist_mu_improved)), ylist_mu_improved, color="#d3d3d3", edgecolor="k", hatch='\\', label="FIFO Mutator Time")
  plt.bar(range(len(ylist_gc_improved)), ylist_gc_improved, bottom=ylist_mu_improved, color='#696969', edgecolor="k", hatch='\\', label="FIFO GC Time")
  plt.xticks(range(len(xlist)), xlist, fontsize=26)#, rotation=30)
  plt.xlim([0, len(xlist)])
  plt.ylim([0,4])
  plt.legend(loc="upper center",fontsize=26,fancybox=True, ncol=2).get_frame().set_alpha(0.5)
  plt.xlabel("Benchmarks running with different numbers of CPU cores (1,2,4,8,16,32,48)", fontsize=26)
  plt.ylabel("Total execution time normalized to run with the \nCFS scheduler on 1 CPU core", fontsize=26)
  ax = fig.add_subplot(1,1,1)
  ax.set_xticks(minor_ticks, minor=True)
  ax.grid(which='minor', linewidth=0.5, linestyle='-', color='0.75')
#  plt.text(0.52,1.03,'1.92', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
#  plt.text(0.6,1.03,'2.03', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
#  plt.text(0.85,1.03,'1.72', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
#  plt.text(0.95,1.03,'3.48  7.32', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
  plt.text(0.05,1.03,'16.8', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top', fontsize=20)
  plt.text(0.7,1.03,'11.6   8.11   4.62', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top', fontsize=20)
  plt.savefig("gc_mutator_cfsbetter.png", bbox_inches='tight')
  plt.cla()

def plot(gcdict, mutatordict):
  namelist = []
  j = -1
  xlist = []
  ylist1 = []  # GC
  ylist2 = []  # mutator
  ylist11 = []
  ylist22 = []
  namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython', 'scalac', 'scaladoc', 'scalatest']
  for name in namelist:
    j += 1
    xlist.append('1\n'+name)
    xlist.append('2')
    xlist.append('4')
    xlist.append('8')
    xlist.append('16')
    xlist.append('32')
    xlist.append('48')
    xlist.append(' ')
    list1 = []
    list2 = []
    list11 = []
    list22 = []

#    eachplot(name, gcdict[name], mutatordict[name])

    list1 = gcdict[name]
    list2 = mutatordict[name]
    list11 = gcdict[name]
    list22 = mutatordict[name]
    # only consider ParallelGC Thread is 2
    base = list1[0] + list2[0]
    for i in range(len(list1)):
      list1[i] = float(list1[i])/float(base)
      list2[i] = float(list2[i])/float(base)
      base2 = list11[i] + list22[i]
      list11[i] = float(list11[i])/base2
      list22[i] = float(list22[i])/base2
      ylist1.append(list1[i])
      ylist2.append(list2[i])
      ylist11.append(list11[i])
      ylist22.append(list22[i])
    ylist1.append(0.0)
    ylist2.append(0.0)
    ylist11.append(0.0)
    ylist22.append(0.0)
  del xlist[-1]
  del ylist1[-1]
  del ylist2[-1]
  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist22)), ylist22, color="#d3d3d3", label="Completion Time")
  plt.bar(range(len(ylist11)), ylist11, bottom=ylist22, color='#000000', label="Pause Time")
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.legend(loc="upper center", ncol=2)
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Fraction of GC and mutator in total")
  plt.savefig("gcfraction.pdf", format='pdf', bbox_inches='tight')
  plt.cla()
'''
  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist2)), ylist2, color="#d3d3d3", label="Completion Time")
  plt.bar(range(len(ylist1)), ylist1, bottom=ylist2, color='#000000', label="Pause Time")
  plt.grid()
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.legend(loc="upper center", ncol=2)
#  plt.gca()
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Execution time normalized to single-thread execution")
  plt.savefig("mutator_GC_overall_performance.pdf", format='pdf', bbox_inches='tight')
  plt.cla()

  plt.figure(0, figsize=(20, 10))
  ylist = []
  for i in range(len(ylist1)):
    ylist.append(ylist1[i]+ylist2[i])
  plt.bar(range(len(ylist)), ylist, color="#d3d3d3")
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.grid()
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Execution time normalized to single-thread execution")
  plt.savefig("overall_performance.pdf", format='pdf', bbox_inches='tight')
  plt.cla()
'''

markerlist = ['.', ',', 'o', 'v', '^', '*', '<', '>', 's', 'p', 'x', 'D']
def lineplot(gcfreqdict):
  namelist = []
  i = -1
  xlist = ['1', '2', '4', '8', '16', '32', '48']
  ylist = []
  for name in gcfreqdict:
    i += 1
    ylist = []
    namelist.append(name)
    base = gcfreqdict[name][0]
    for gc in gcfreqdict[name]:
      ylist.append(float(gc/base))
    plt.figure(0)
    plt.plot(range(len(ylist)), ylist, marker=markerlist[i], color='#d3d3d3',label=name)
    plt.savefig("GC_Frequency.pdf", format='pdf', bbox_inches='tight')
  plt.figure(0)
  plt.xticks(range(len(xlist)), xlist)
  plt.ylabel("Number of GC")
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.legend(loc="upper left", ncol=3)
  plt.savefig("GC_Frequency.pdf", format='pdf', bbox_inches='tight')
  plt.cla()

def main():
  try:
    script, filename = sys.argv
  except:
    sys.exit("Usage: Filepath needed\n")
  gcdict_default = {}
  mutatordict_default = {}
  gcdict_fifo = {}
  mutatordict_fifo = {}
  gcdict_improved = {}
  mutatordict_improved = {}
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
            (gctime, mutatortime, gcfrequency) = helper(f)
            name = (f.split('_')[-2]).split('/')[-1]
            threadid = f.split('_')[-1]
            index = thread.index(threadid)
            if default == True:
              if not name in gcdict_default:
                gcdict_default[name] = [0, 0, 0, 0, 0, 0, 0]
                mutatordict_default[name] = [0, 0, 0, 0, 0, 0, 0]
              gcdict_default[name][index] = gctime
              mutatordict_default[name][index] = mutatortime
            elif fifo == True:
              if not name in gcdict_fifo:
                gcdict_fifo[name] = [0, 0, 0, 0, 0, 0, 0]
                mutatordict_fifo[name] = [0, 0, 0, 0, 0, 0, 0]
              gcdict_fifo[name][index] = gctime
              mutatordict_fifo[name][index] = mutatortime
            else:
              if not name in gcdict_improved:
                gcdict_improved[name] = [0, 0, 0, 0, 0, 0, 0]
                mutatordict_improved[name] = [0, 0, 0, 0, 0, 0, 0]
              gcdict_improved[name][index] = gctime
              mutatordict_improved[name][index] = mutatortime

#  for name in gcdict_default:
#    print name
#    print gcdict_default[name]
#    print mutatordict_default[name]
#  plot_gc(gcdict_default, mutatordict_default, gcdict_fifo, mutatordict_fifo, gcdict_improved, mutatordict_improved)
  plot2(gcdict_default, mutatordict_default, gcdict_fifo, mutatordict_fifo)
#  print gcdict_default['lusearch'], mutatordict_default['lusearch']
#  print gcdict_fifo['lusearch'], mutatordict_fifo['lusearch']
#  lineplot(gcfreqdict)

if __name__ == "__main__":
  main()
