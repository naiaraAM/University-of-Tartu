#!/bin/bash

# Measure the time taken by grep
echo "Measuring grep..."
/usr/bin/time -p -o grep_time.txt grep 'aaa' random_text.txt > /dev/null

# Measure the time taken by awk
echo "Measuring awk..."
/usr/bin/time -p -o awk_time.txt awk '/aaa/' random_text.txt > /dev/null

# Measure the time taken by sed
echo "Measuring sed..."
/usr/bin/time -p -o sed_time.txt sed -n '/aaa/p' random_text.txt > /dev/null