import pytest
from fastapi.testclient import TestClient
from main import app
from database import engine
from sqlmodel import SQLModel

client = TestClient(app)

# clear and rebuild the dataset before every testing
@pytest.fixture(name="session", autouse=True)
def session_fixture():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def test_start_ride():
    response = client.post("/ride/start?user_id=user123")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user123"
    assert data["is_active"] is True

def test_prevent_duplicate_active_ride():
    client.post("/ride/start?user_id=user123")
    response = client.post("/ride/start?user_id=user123")
    assert response.status_code == 400
    assert response.json()["detail"] == "User already has an active ride"

def test_pricing_logic_under_15_mins():
    # start
    start_res = client.post("/ride/start?user_id=test_user")
    ride_id = start_res.json()["id"]
    # simulation end（the test run fast, so the time must be less than 15 mins）
    end_res = client.post(f"/ride/end/{ride_id}")
    assert end_res.json()["total_cost"] == 5.0 # unlock fee only