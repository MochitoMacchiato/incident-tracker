incidents = [
  {"id": 1, "title": "API timeout", "severity": "high", "status": "open"},
  {"id": 2, "title": "Disk almost full", "severity": "medium", "status": "open"},
  {"id": 3, "title": "Typo on status page", "severity": "low", "status": "closed"},
  {"id": 4, "title": "DB connection errors", "severity": "high", "status": "closed"},
  {"id": 5, "title": "Slow login", "severity": "medium", "status": "open"}
]

def count_by_severity(incidents):
    severity_count = {}
    
    for incident in incidents:
        incident_severity = incident["severity"]
        severity_count[incident_severity] = severity_count.get(incident_severity, 0) + 1
    return severity_count

def open_titles(incidents):
    return [incident["title"] for incident in incidents if incident["status"] == "open"]

def id_to_title(incidents):
    return {incident["id"]: incident["title"] for incident in incidents}

if __name__ == "__main__":
    print(count_by_severity(incidents))
    print(open_titles(incidents))
    print(id_to_title(incidents))
