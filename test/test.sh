#! /bin/sh

BIN=bin
OUTPUT=output

if [ "$1" == "--no-color" ]; then
  shift
else
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  NOCOLOR='\033[0;0m'
fi

if [ "$#" -eq "0" ]; then
  bins="$BIN/*"
else
  bins="$*"
fi

for f in $bins; do
  base="$(echo "$f" | sed -e "s/^$BIN\///")"
  output="$OUTPUT/${base}.out"
  if [ -f "$output" ]; then
    dif="$($(realpath "$f") | diff - "$output")"
    if [ -z "$dif" ]; then
      echo "$base ${GREEN}PASSED${NOCOLOR}"
    else
      echo "$dif"
      echo "$base ${RED}FAILED${NOCOLOR}"
      allclear="$allclear $base"
    fi
  fi
done

echo "====="
if [ -z "$allclear" ]; then
  echo "All tests ${GREEN}PASSED${NOCOLOR}"
else
  echo "The following tests ${RED}FAILED${NOCOLOR}"
  for f in $allclear; do
    echo " * $f"
  done
  exit 1
fi
