from incidents_basics import count_by_severity
import sys
import json

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = "drills/incidents.json"

try:
    with open(path) as file:
        incidents = json.load(file)
except FileNotFoundError:
    print(f"Error: file not found: {path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: invalid JSON in {path}")
    sys.exit(1)

counts = count_by_severity(incidents)
lines = [f"Total: {len(incidents)}"]
for severity, count in counts.items():
    lines.append(f"{severity}: {count}")
report = "\n".join(lines)

print(report)
with open("drills/summary.txt", "w") as file:
    file.write(report + "\n")
