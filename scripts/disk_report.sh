#! /bin/bash
# disk_report.sh - print a short disk usage report

echo "-------- Disk Usage Report --------"
echo "Date:$(date)"
echo

echo "-------- Root Filesystem Usage --------"
df -h /
echo

echo "-------- 5 Biggest Items in your Home Folder --------"
du -sh ~/* 2>/dev/null | sort -rh | head -5
echo

usage=$(df / --output=pcent | tail -1 | tr -dc '0-9')
   if [ "$usage" -ge 80 ]; then
         echo "WARNING: / is ${usage}% full"
   else
         echo "OK: / ${usage}% full"
fi    