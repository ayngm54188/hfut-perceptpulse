import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    print("[Test] Root endpoint OK")

def test_get_items():
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["total"] > 0
    print(f"[Test] Items endpoint OK. Found {data['total']} items.")

def test_stats_summary():
    response = client.get("/api/v1/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] > 0
    print(f"[Test] Stats endpoint OK: {data}")

if __name__ == "__main__":
    test_root()
    test_get_items()
    test_stats_summary()
    print("All backend sanity tests passed!")
