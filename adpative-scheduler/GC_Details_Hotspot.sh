#!/bin/bash
#
# thread_same_gc.sh
# script to run the benchmark with different thread numbers, but same GC numbers with changable heap size

# define the Logfile
#LOGFILE=/home/jqian/projects/jvm_cache_management/work-folder/thread_and_GC/log_
if [ ! -d "./results" ]; then
  mkdir results
fi

dir=$PWD
LOGFILE=$dir/results/

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# define JikesRVM/benchmark path
Jikes=/home/jqian/projects/tools/JikesRVM/jikesrvm-3.1.3/dist/working/production_x86_64-linux/rvm
Jikes_PMU=/home/jqian/projects/jvm_cache_management/work-folder/jikesrvm-3.1.3-production-perfevent/dist/working/production_x86_64-linux/rvm

Dacapo=/home/jqian/benchmarks/dacapo-9.12-bach.jar
SPECJVM_dir=/home/jqian/benchmarks/SPECjvm2008
SPECJVM_jar=/home/jqian/benchmarks/SPECjvm2008/SPECjvm2008.jar

# declare the associated array, benchmark-heap_size
# this is bash-4, supports associate array
declare -A dacapobenchmark
dacapobenchmark=(["eclipse"]="330m" ["jython"]="90m" ["lusearch"]="90m" ["pmd"]="210m" ["sunflow"]="210m" ["avrora"]="75m" ["xalan"]="150m" ["h2"]="900m" ["tomcat"]="135m")

declare -A specbenchmark
#specbenchmark=(["compiler.sunflow"]="6000m" ["crypto.aes"]="2000m" ["scimark.fft.large"]="4000m" ["xml.validation"]="2000m" ["xml.transform"]="2000m")
specbenchmark=(["compiler.compiler"]="2000m" ["compress"]="1000m" ["crypto.signverify"]="1500m" ["mpegaudio"]="1500m", ["compiler.sunflow"]="6000m" ["crypto.aes"]="2000m" ["scimark.fft.large"]="4000m" ["xml.validation"]="2000m" ["xml.transform"]="2000m")
# ["derby"]="3000m")

function exe {
    set -x
    $Jikes -Xmx$1 -Xms$1 -verbose:gc -jar $Dacapo $name -t $thread >> $LOGFILE
    set +x
    echo "==============================" >> $LOGFILE
}

for thread in 1 2 4 8 16 32 48
do
	if [ $thread -eq 1 ]; then
		python set_cpus.py 0
	elif [ $thread -eq 2 ]; then
		python set_cpus.py 0-1
	elif [ $thread -eq 4 ]; then
		python set_cpus.py 0-3
	elif [ $thread -eq 8 ]; then
		python set_cpus.py 0-7
	elif [ $thread -eq 16 ]; then
		python set_cpus.py 0-15
	elif [ $thread -eq 32 ]; then
		python set_cpus.py 0-31
	elif [ $thread -eq 48 ]; then
		python set_cpus.py 0-47
	fi
	for i in {1..3}
	do
		for name in "${!dacapobenchmark[@]}"
		do
        	echo "$name-${dacapobenchmark["$name"]}"
		#python /home/jqian/multi-threading/adpative-scheduler/adaptive_sched.py
		chrt -f 99 java -Xms${dacapobenchmark["$name"]} -Xmx${dacapobenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCApplicationStoppedTime -XX:+UseParallelGC -Xloggc:$LOGFILE"$name"_"$thread"_"$i" -jar $Dacapo $name -t 64 >> $LOGFILE"$name"_"$thread"
	        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $LOGFILE"$name"_"$thread"
		done
	done
done

cd $SPECJVM_dir

for thread in 1 2 4 8 16 32 48
do
   if [ $thread -eq 1 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0
   elif [ $thread -eq 2 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0-1
   elif [ $thread -eq 4 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0-3
   elif [ $thread -eq 8 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0-7
   elif [ $thread -eq 16 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0-15
   elif [ $thread -eq 32 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0-31
   elif [ $thread -eq 48 ]; then
      python /home/jqian/multi-threading/adpative-scheduler/set_cpus.py 0-47
   fi
   for i in {1..3}; do
      for name in "${!specbenchmark[@]}"; do
        echo "$name-${specbenchmark["$name"]}-$thread-$i"
        #python /home/jqian/multi-threading/adpative-scheduler/adaptive_sched.py
	chrt -f 99 java -Xms${specbenchmark["$name"]} -Xmx${specbenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCApplicationConcurrentTime -XX:+PrintGCApplicationStoppedTime -XX:+UseParallelGC -Xloggc:$LOGFILE"$name"_"$thread"_"$i" -jar $SPECJVM_jar $name -bt 64 -ops 10 &>> $LOGFILE"$name"_"$thread"
        echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> $LOGFILE"$name"_"$thread"
      done
   done
done
