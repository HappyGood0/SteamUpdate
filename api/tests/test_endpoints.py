import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test du endpoint /api/health"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommend_endpoint_valid():
    """Test du endpoint /api/recommend avec une requête valide"""
    response = client.post("/api/recommend", json={"steam_id": "76561198167767436"})
    assert response.status_code == 200
    data = response.json()
    assert "steam_id" in data
    assert "recommendations" in data
    assert data["steam_id"] == "76561198167767436"
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0


def test_recommend_endpoint_missing_steam_id():
    """Test du endpoint /api/recommend sans steam_id"""
    response = client.post("/api/recommend", json={})
    assert response.status_code == 422  # Validation error


def test_recommend_endpoint_invalid_payload():
    """Test du endpoint /api/recommend avec payload invalide"""
    response = client.post("/api/recommend", json={"invalid": "data"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_metrics_exposed():
    """Test que les métriques Prometheus sont exposées"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "Health_check_requests_total" in response.text
