#!/bin/bash
# error_counter.sh - script that takes a log file path, then prints total lines, ERROR count, WARN count, and the most common error messages.
# Usage: ./error_counter.sh <logfile>

logfile="$1"

if [ ! -f "$logfile" ]; then
    echo "Usage: $0 <logfile>"
    echo "File not found: '$logfile'"
    exit 1
fi

total=$(wc -l < "$logfile")
error=$(grep -c ERROR "$logfile")
warn=$(grep -c WARN "$logfile")

echo  "=== Log summary: $logfile ==="
echo "Total lines: $total"
echo "ERROR lines: $error"
echo "WARN lines: $warn"
echo
echo "--- Top error messages ---"
grep ERROR "$logfile" | sed 's/^[^ ]* [^ ]* //' | sort | uniq -c | sort -rn | head -5