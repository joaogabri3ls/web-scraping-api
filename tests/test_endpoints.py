from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_news():
    response = client.get("/news")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_download_csv():
    response = client.get("/news/csv")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv"

def test_download_pdf():
    response = client.get("/news/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
