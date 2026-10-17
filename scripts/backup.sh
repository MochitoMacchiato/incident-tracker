#!/bin/bash
# backup.sh - make a timestamped .tar.gz backup of a folder
# Usage: ./backup.sh <source_dir> [backup_dir]
# Default backup_dir is ~/backups

source_dir="$1"
backup_dir="${2:-$HOME/backups}"

if [ ! -d "$source_dir" ]; then
    echo "Usage: $0 <source_dir> [backup_dir]"
    echo "Folder not found: '$source_dir'"
    exit 1
fi

source_dir=$(realpath "$source_dir")
mkdir -p "$backup_dir"

timestamp=$(date +%Y-%m-%d_%H-%M-%S)
name=$(basename "$source_dir")
archive="$backup_dir/${name}_${timestamp}.tar.gz"

tar -czf "$archive" -C "$(dirname "$source_dir")" "$name"

echo "Backup create: $archive"
ls -lh "$archive"
echo "First entries inside:"
tar -tzf "$archive" | head -10
