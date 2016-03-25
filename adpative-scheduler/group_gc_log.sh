#/bin/bash

if [[ $# -lt 2 ]]; then
  echo "src dir and des dir are needed."
  exit 0
fi

srcdir=$1
desdir=$2

for benchmark in "lusearch" "xalan" "sunflow" "h2" "eclipse" "jython" "eclipse" "pmd" \
    "avrora" "tomcat" "compiler.compiler" "compress" "crypto.signverify" "mpegaudio" \
    "compiler.sunflow" "crypto.aes" "scimark.fft.large" "xml.validation" "xml.transform"; do
  for thread in 1 2 4 8 16 32 48; do
    for i in {1..3}; do
      cat "${srcdir}"/"${benchmark}"_"${thread}"_"${i}" >> "${desdir}"/"${benchmark}"_"${thread}"
      echo "%%%%%%%%%%%%%%%%%%%%%%%" >> "${desdir}"/"${benchmark}"_"${thread}"
    done
  done
done
