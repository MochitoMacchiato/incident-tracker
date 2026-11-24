import pytest

@pytest.fixture
def created_incident(client):
    payload = {
        "title": "Try lang test_incident",
        "description": "Testing lang toh tol",
        "severity": "high",
        "status": "open",
        "service_id": 1,
    }

    response = client.post("/incidents", json=payload)

    assert response.status_code == 201
    return response.json()


def test_create_incident(client):
    payload = {
        "title": "Try lang test_incident",
        "description": "Testing lang toh tol",
        "severity": "high",
        "status": "open",
        "service_id": 1,
    }
    r = client.post("/incidents", json=payload)

    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Try lang test_incident"
    assert body["severity"] == "high"
    assert "id" in body

def test_create_incident_unknown_service(client):
    payload = {
        "title": "Create an unknown incident",
        "description": "Trying to create an unknown incident test",
        "severity": "high",
        "status": "open",
        "service_id": 9999,
    }

    r = client.post("/incidents", json=payload)

    assert r.status_code == 404

@pytest.mark.parametrize(
    "bad_body",
    [
        {"description": "no title", "severity": "high", "service_id": 1},
        {"title": "", "severity": "high", "service_id": 1},
        {"title": "x", "severity": "banana", "service_id": 1},        
    ],
    ids=["missing-title", "empty-title", "bad-severity"]
)
def test_create_incident_invalid_body(client, bad_body):
    r = client.post("/incidents", json=bad_body)

    assert r.status_code == 422

def test_list_incidents_empty(client):
    r = client.get("/incidents")

    assert r.status_code == 200
    assert r.json() == []

def test_list_incidents_after_create(client, created_incident):
    r = client.get("/incidents")

    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["id"] == created_incident["id"]


def test_get_incident(client, created_incident):
    incident_id = created_incident["id"]
    r = client.get(f"/incidents/{incident_id}")

    assert r.status_code == 200
    assert r.json()["id"] == incident_id
    assert r.json()["title"] == created_incident["title"]

def test_get_unknown_incident(client):
    r = client.get("/incidents/999")

    assert r.status_code == 404


def test_update_incident(client, created_incident):
    incident_id = created_incident["id"]
    r = client.patch(f"/incidents/{incident_id}", json={"status": "resolved"})

    assert r.status_code == 200
    assert r.json()["status"] == "resolved"
    assert r.json()["title"] == created_incident["title"]

def test_update_unknown_incident(client):
    r = client.patch("/incidents/9999", json={"status": "resolved"})

    assert r.status_code == 404

def test_update_title_null(client, created_incident):   
    incident_id = created_incident["id"]
    r = client.patch(f"/incidents/{incident_id}", json={"title": None})

    assert r.status_code == 422
    assert r.json()["detail"] == "title cannot be null"


def test_delete_incident(client, created_incident):
    incident_id = created_incident["id"]
    r = client.delete(f"/incidents/{incident_id}")

    assert r.status_code == 204
    r = client.get(f"/incidents/{incident_id}")

    assert r.status_code == 404

def test_delete_unknown_incident(client):
    r = client.delete("/incidents/9999")

    assert r.status_code == 404