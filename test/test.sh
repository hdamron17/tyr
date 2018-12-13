#! /bin/bash

BIN=bin
OUTPUT=output

if [ "$#" -eq "0" ]; then
  bins="$BIN/*"
else
  bins="$*"
fi

for f in $bins; do
  base="$(echo "$f" | sed -e "s/^$BIN\///")"
  output="$OUTPUT/${base}.out"
  dif="$($(realpath "$f") | diff - $output)"
  if [ -z "$dif" ]; then
    echo "$base PASSED"
  else
    echo "$dif"
    echo "$base FAILED"
    allclear="$allclear $base"
  fi
done

echo "====="
if [ -z "$allclear" ]; then
  echo "All tests PASSED"
else
  echo "The following tests FAILED"
  for f in $allclear; do
    echo " * $f"
  done
fi
