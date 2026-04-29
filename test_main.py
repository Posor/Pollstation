# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test de GET /stats
def test_stats_endpoint():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "polls" in data # On vérifie que la clé "polls" est présente dans la réponse
    assert "votes" in data # On vérifie que la clé "votes" est présente dans la réponse

# Test de la création d'un sondage (doit échouer si il y a moins de 2 options)
def test_create_poll_validation():
    response = client.post(
        "/polls",
        json={"question": "Test?", "options": ["Option 1"]}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "A poll must have at least 2 options."

# Test de la validation Pydantic (doit échouer si la question fait moins de 3 caractères)
def test_pydantic_min_length():
    response = client.post(
        "/polls",
        json={"question": "Ab", "options": ["Oui", "Non"]}
    )
    assert response.status_code == 422

# Test de la pagination (bonus)
def test_pagination_logic():
    response = client.get("/polls?limit=1") # On demande une limite de 1 sondage
    assert response.status_code == 200
    assert len(response.json()) <= 1 # On vérifie que la limite est respectée