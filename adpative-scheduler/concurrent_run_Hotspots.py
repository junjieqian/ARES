#!/usr/bin/python

import string
import subprocess

if __name__ == "__main__":
  import sys
  import os
  import pickle

  if len(sys.argv) < 5:
    sys.exit("USAGE: python %s java -jar ../dacapo-9.12-rc1-bach.jar pmd"%sys.argv[0])
  
  stdin = open("/dev/null")
  stdout = open("/tmp/stdout", "w")
  # name = sys.argv[3]

  fifo_jvm = sys.argv[1:]
  fifo_jvm[8] += "_fifo"
  cfs_jvm = sys.argv[1:]
  cfs_jvm[8] += "_cfs"

  command_1 = ["chrt", "-f", "10"].append(fifo_jvm)
  command_2 = ["chrt", "-r", "10"].append(cfs_jvm)
  print command_1
  print command_2
  process_1 = subprocess.Popen(command_1, stdin = stdin, stdout = stdout)
  process_2 = subprocess.Popen(command_2, stdin = stdin, stdout = stdout)