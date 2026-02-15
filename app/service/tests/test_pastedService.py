# integration Test for the entire service, plus the http endpoint.

# It glues everything together ergonomically, thanks to powerful library
# "pytest" and amazing testing capabelities by SQLModel and FastAPI

from sqlmodel import SQLModel, Session, StaticPool, create_engine
import pytest
from fastapi.testclient import TestClient
from app.db import get_session
from app.main import app
from app.service.adminService import get_admin_service


@pytest.fixture(name="session")
def session_fixture():

    # Presumably, we're cheating a little bit by using sqlite instead of
    # postgresql. But it's better then nothing.
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_pasted_success(client: TestClient):
    # 1. Create
    response = client.post(
        "/pastes", json={"content": "lorem ipsum dolor", "duration": "0"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == "lorem ipsum dolor"

    # 2. Now, fetch the result.
    id = data["id"]
    response = client.get(f"/pastes/{id}")

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == "lorem ipsum dolor"


# def test_create_paste_failure():
