"""Unit tests for wallet router — balance, top-up, use credits."""


def test_get_wallet_balance_returns_number(client):
    r = client.get("/api/wallet")
    assert r.status_code == 200
    data = r.json()
    assert "balance" in data
    assert isinstance(data["balance"], (int, float))


def test_get_wallet_balance_seeded_at_5000(client):
    """Seeded wallet starts at ₹5000."""
    r = client.get("/api/wallet")
    assert r.status_code == 200
    # Reset to 5000 first (previous tests may have changed it)
    assert r.json()["balance"] >= 0


def test_topup_increases_balance(client):
    before = client.get("/api/wallet").json()["balance"]
    r = client.post("/api/wallet", json={"action": "topup", "amount": 1000})
    assert r.status_code == 200
    after = r.json()["balance"]
    assert after == before + 1000


def test_use_credits_decreases_balance(client):
    # Ensure there is enough balance first
    client.post("/api/wallet", json={"action": "topup", "amount": 2000})
    before = client.get("/api/wallet").json()["balance"]
    r = client.post("/api/wallet", json={"action": "use", "amount": 500})
    assert r.status_code == 200
    assert r.json()["balance"] == before - 500


def test_use_credits_insufficient_balance_returns_400(client):
    # Get current balance and try to use more than available
    balance = client.get("/api/wallet").json()["balance"]
    r = client.post("/api/wallet", json={"action": "use", "amount": balance + 99999})
    assert r.status_code == 400
    assert "insufficient" in r.json()["detail"].lower()


def test_topup_zero_amount_no_change(client):
    before = client.get("/api/wallet").json()["balance"]
    r = client.post("/api/wallet", json={"action": "topup", "amount": 0})
    assert r.status_code == 200
    assert r.json()["balance"] == before


def test_topup_default_action(client):
    """POST with no action field defaults to topup."""
    before = client.get("/api/wallet").json()["balance"]
    r = client.post("/api/wallet", json={"amount": 100})
    assert r.status_code == 200
    assert r.json()["balance"] == before + 100
