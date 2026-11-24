import os

TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Service

assert make_url(TEST_DATABASE_URL).database.endswith("_test"), (
    "TEST_DATABASE_URL must point at a database whose name ends in _test"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


@pytest.fixture
def client():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    with TestingSessionLocal() as session:
        session.add(Service(name="payments"))
        session.commit()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)
