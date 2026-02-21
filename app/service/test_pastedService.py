# integration Test for the entire service, plus it's http endpoint.

# It glues everything together ergonomically, thanks to powerful library
# "pytest" and amazing testing capabelities provided by SQLModel and FastAPI

from fastapi import status
from sqlmodel import SQLModel, Session, StaticPool, create_engine, select
import pytest
from fastapi.testclient import TestClient
from app.db import get_session
from app.main import app
from app.models.pasted import Pasted


# Presumably, we're cheating a little bit by using sqlite instead of
# postgresql. But it's better then nothing.
@pytest.fixture(name="session")
def session_fixture():
    """Sets up the session for testing. Does the table creation."""

    # Using `StaticPool` will help us maintain a single in-memory database to
    # every test function.
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

    assert response.status_code == 201
    assert data["content"] == "lorem ipsum dolor"

    # 2. Now, fetch the result.
    shortcode = data["shortcode"]
    response = client.get(f"/pastes/?shortcode={shortcode}")

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == "lorem ipsum dolor"


def test_create_paste_failure(client: TestClient):
    ## Should endup with validation error.
    response = client.post(
        "/pastes",
        json={
            "content": "lorem ipsum dolor",
            "duration": "41148",
        },  # duration value is invalid.
    )

    # assert response.status_code != 200
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_view_count_logic(client: TestClient, session: Session):
    # 1. Create
    response = client.post("/pastes", json={"content": "rabio", "duration": "0"})

    data = response.json()

    assert response.status_code == 201
    assert data["content"] == "rabio"

    shortcode = data["shortcode"]

    response = client.get(f"/pastes/?shortcode={shortcode}")

    statement = select(Pasted).where(Pasted.shortcode == shortcode)
    pasted_item = session.exec(statement).first()

    assert pasted_item
    assert pasted_item.view_count == 1
