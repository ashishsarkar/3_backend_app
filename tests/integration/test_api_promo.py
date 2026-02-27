"""Integration tests: promo validation API."""


def test_validate_valid_percent_promo(client):
    r = client.post("/api/promo/validate", json={"code": "SAVE10", "amount": 3000})
    assert r.status_code == 200
    data = r.json()
    assert data["valid"] is True
    assert data["savings"] == 300
    assert "%" in data["message"]


def test_validate_valid_fixed_promo(client):
    r = client.post("/api/promo/validate", json={"code": "FLAT500", "amount": 5000})
    assert r.status_code == 200
    data = r.json()
    assert data["valid"] is True
    assert data["savings"] == 500
    assert "500" in data["message"]


def test_validate_welcome_promo(client):
    r = client.post("/api/promo/validate", json={"code": "WELCOME", "amount": 2000})
    assert r.status_code == 200
    data = r.json()
    assert data["valid"] is True
    assert data["savings"] == 200


def test_validate_unknown_code(client):
    r = client.post("/api/promo/validate", json={"code": "BADCODE", "amount": 1000})
    assert r.status_code == 200
    assert r.json()["valid"] is False


def test_validate_lowercase_code_accepted(client):
    """Codes should be case-insensitive."""
    r = client.post("/api/promo/validate", json={"code": "flat500", "amount": 2000})
    assert r.status_code == 200
    assert r.json()["valid"] is True


def test_validate_save10_max_cap_500(client):
    """10% of 20,000 = 2,000 but capped at 500."""
    r = client.post("/api/promo/validate", json={"code": "SAVE10", "amount": 20000})
    assert r.status_code == 200
    assert r.json()["savings"] == 500


def test_validate_fixed_discount_not_exceed_amount(client):
    """FLAT500 on ₹100 should save only ₹100 (can't save more than total)."""
    r = client.post("/api/promo/validate", json={"code": "FLAT500", "amount": 100})
    assert r.status_code == 200
    assert r.json()["savings"] == 100


def test_validate_response_includes_code(client):
    r = client.post("/api/promo/validate", json={"code": "SAVE10", "amount": 1000})
    assert r.json()["code"] == "SAVE10"


def test_validate_empty_body_returns_invalid(client):
    r = client.post("/api/promo/validate", json={})
    assert r.status_code == 200
    assert r.json()["valid"] is False
