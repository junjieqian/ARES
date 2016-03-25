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
  namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython', 'eclipse', 'pmd', \
  'avrora', 'tomcat', 'compiler.sunflow', 'crypto.aes', 'scimark.fft.large', 'xml.validation', 'xml.transform']
  for name in namelist:
    j += 1
    xlist.append('1\n' + name)
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
    base = list1[0] + list2[0]
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
  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist_mu_default)), ylist_mu_default, color="#5f9ea0", edgecolor="k", label="Existing Completion Time")
  plt.bar(range(len(ylist_gc_default)), ylist_gc_default, bottom=ylist_mu_default, color='#0000ff', \
    edgecolor="k", label="Existing Pause Time")
  plt.bar(range(len(ylist_mu_fifo)), ylist_mu_fifo, color="#d3d3d3", edgecolor="k", label="FIFO Completion Time")
  plt.bar(range(len(ylist_gc_fifo)), ylist_gc_fifo, bottom=ylist_mu_fifo, color='#696969', edgecolor="k", label="FIFO Pause Time")
  plt.bar(range(len(ylist_mu_improved)), ylist_mu_improved, color="#d3d3d3", edgecolor="k", hatch='\\', label="Improved Completion Time")
  plt.bar(range(len(ylist_gc_improved)), ylist_gc_improved, bottom=ylist_mu_improved, color='#696969', edgecolor="k", \
    hatch='\\', label="Improved Pause Time")
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.ylim([0, 2])
  plt.legend(loc="upper center", ncol=3)
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Fraction of GC and mutator in total")
  plt.savefig("gcfraction.pdf", format='pdf', bbox_inches='tight')
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
  namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython', 'eclipse', 'pmd', \
  'avrora', 'tomcat', 'compiler.sunflow', 'crypto.aes', 'scimark.fft.large', 'xml.validation', 'xml.transform']
  for name in namelist:
    j += 1
    xlist.append(name)
    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    xlist.append(' ')
    list1 = gcdict_default[name]
    list2 = mutatordict_default[name]
    list3 = gcdict_fifo[name]
    list4 = mutatordict_fifo[name]
    list5 = gcdict_improved[name]
    list6 = mutatordict_improved[name]
    base = list1[0] + list2[0]
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

    ylist_gc_default.append(0.0)
    ylist_mu_default.append(0.0)
    ylist_gc_fifo.append(0.0)
    ylist_mu_fifo.append(0.0)
  del xlist[-1]
  del ylist_gc_default[-1]
  del ylist_mu_default[-1]
  del ylist_mu_fifo[-1]
  del ylist_gc_fifo[-1]
  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist_mu_default)), ylist_mu_default, color="#5f9ea0", edgecolor="k", label="Existing Completion Time")
  plt.bar(range(len(ylist_gc_default)), ylist_gc_default, bottom=ylist_mu_default, color='#0000ff', \
    edgecolor="k", label="Existing Pause Time")
  plt.bar(range(len(ylist_mu_fifo)), ylist_mu_fifo, color="#d3d3d3", edgecolor="k", label="FIFO Completion Time")
  plt.bar(range(len(ylist_gc_fifo)), ylist_gc_fifo, bottom=ylist_mu_fifo, color='#696969', edgecolor="k", label="FIFO Pause Time")
  plt.bar(range(len(ylist_mu_improved)), ylist_mu_improved, color="#d3d3d3", edgecolor="k", hatch='\\', label="Improved Completion Time")
  plt.bar(range(len(ylist_gc_improved)), ylist_gc_improved, bottom=ylist_mu_improved, color='#696969', edgecolor="k", \
    hatch='\\', label="Improved Pause Time")
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.ylim([0, 2])
  plt.legend(loc="upper center", ncol=3)
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Fraction of GC and mutator in total")
  plt.savefig("gcfraction.pdf", format='pdf', bbox_inches='tight')
  plt.cla()
