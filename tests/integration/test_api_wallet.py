"""Integration tests: wallet API — balance, top-up, use credits."""


def _reset_wallet(client, target=5000):
    """Reset wallet to a known balance for predictable tests."""
    current = client.get("/api/wallet").json()["balance"]
    diff = target - current
    if diff > 0:
        client.post("/api/wallet", json={"action": "topup", "amount": diff})
    elif diff < 0:
        client.post("/api/wallet", json={"action": "use", "amount": abs(diff)})


def test_get_wallet_returns_balance(client):
    r = client.get("/api/wallet")
    assert r.status_code == 200
    assert "balance" in r.json()
    assert isinstance(r.json()["balance"], (int, float))


def test_topup_increases_balance(client):
    _reset_wallet(client, 1000)
    r = client.post("/api/wallet", json={"action": "topup", "amount": 500})
    assert r.status_code == 200
    assert r.json()["balance"] == 1500


def test_use_credits_decreases_balance(client):
    _reset_wallet(client, 2000)
    r = client.post("/api/wallet", json={"action": "use", "amount": 800})
    assert r.status_code == 200
    assert r.json()["balance"] == 1200


def test_use_credits_exact_balance(client):
    """Using exactly the available balance should bring it to 0."""
    _reset_wallet(client, 300)
    r = client.post("/api/wallet", json={"action": "use", "amount": 300})
    assert r.status_code == 200
    assert r.json()["balance"] == 0


def test_use_credits_more_than_balance_returns_400(client):
    _reset_wallet(client, 100)
    r = client.post("/api/wallet", json={"action": "use", "amount": 500})
    assert r.status_code == 400
    assert "insufficient" in r.json()["detail"].lower()


def test_multiple_topups_accumulate(client):
    _reset_wallet(client, 0)
    client.post("/api/wallet", json={"action": "topup", "amount": 1000})
    client.post("/api/wallet", json={"action": "topup", "amount": 500})
    r = client.get("/api/wallet")
    assert r.json()["balance"] == 1500


def test_topup_then_use_correctly(client):
    _reset_wallet(client, 1000)
    client.post("/api/wallet", json={"action": "topup", "amount": 2000})
    r = client.post("/api/wallet", json={"action": "use", "amount": 1500})
    assert r.status_code == 200
    assert r.json()["balance"] == 1500  # 1000 + 2000 - 1500


def test_balance_persists_after_operations(client):
    _reset_wallet(client, 5000)
    client.post("/api/wallet", json={"action": "use", "amount": 1000})
    r = client.get("/api/wallet")
    assert r.json()["balance"] == 4000
