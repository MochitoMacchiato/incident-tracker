# Manual test notes (incidents CRUD)

| Request | Expected | Actual |
|---|---|---|
| POST valid incident | 201 | |
| POST empty title | 422 | |
| POST severity not in list | 422 | |
| GET existing id | 200 | |
| GET id 99999 | 404 | |
| PATCH status only | 200, other fields unchanged | |
| PATCH id 99999 | 404 | |
| DELETE existing | 204 | |
| DELETE same id again | 404 | |