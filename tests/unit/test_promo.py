"""Unit tests for Promo model discount logic and promo router."""
import pytest


class TestPromoCalcSavings:
    """Tests for Promo.calc_savings — no DB needed."""

    def _make_promo(self, discount_type, discount_value, max_discount=None):
        from app.models import Promo
        p = Promo()
        p.discount_type = discount_type
        p.discount_value = discount_value
        p.max_discount = max_discount
        return p

    # ── Percent discount ─────────────────────────────────────────────────────

    def test_percent_basic(self):
        promo = self._make_promo("percent", 10, max_discount=500)
        assert promo.calc_savings(1000) == 100

    def test_percent_capped_by_max_discount(self):
        promo = self._make_promo("percent", 10, max_discount=500)
        assert promo.calc_savings(10000) == 500

    def test_percent_no_max_discount(self):
        promo = self._make_promo("percent", 20, max_discount=None)
        assert promo.calc_savings(5000) == 1000

    def test_percent_zero_amount(self):
        promo = self._make_promo("percent", 10, max_discount=500)
        assert promo.calc_savings(0) == 0

    # ── Fixed discount ───────────────────────────────────────────────────────

    def test_fixed_basic(self):
        promo = self._make_promo("fixed", 500)
        assert promo.calc_savings(2000) == 500

    def test_fixed_capped_at_amount(self):
        """Fixed discount cannot exceed the total amount."""
        promo = self._make_promo("fixed", 1000)
        assert promo.calc_savings(300) == 300

    def test_fixed_equals_amount(self):
        promo = self._make_promo("fixed", 500)
        assert promo.calc_savings(500) == 500


class TestPromoRouterUnit:
    """Unit tests for promo router via TestClient (uses seeded DB)."""

    def test_validate_invalid_code_returns_valid_false(self, client):
        r = client.post("/api/promo/validate", json={"code": "NOTEXIST", "amount": 1000})
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert "message" in data

    def test_validate_save10_percent_discount(self, client):
        r = client.post("/api/promo/validate", json={"code": "SAVE10", "amount": 3000})
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is True
        assert data["code"] == "SAVE10"
        assert data["savings"] == 300  # 10% of 3000, capped at 500

    def test_validate_save10_capped_at_500(self, client):
        r = client.post("/api/promo/validate", json={"code": "SAVE10", "amount": 10000})
        assert r.status_code == 200
        data = r.json()
        assert data["savings"] == 500  # max_discount cap

    def test_validate_flat500_fixed_discount(self, client):
        r = client.post("/api/promo/validate", json={"code": "FLAT500", "amount": 5000})
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is True
        assert data["savings"] == 500

    def test_validate_welcome_discount(self, client):
        r = client.post("/api/promo/validate", json={"code": "WELCOME", "amount": 1000})
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is True
        assert data["savings"] == 200

    def test_validate_code_case_insensitive(self, client):
        r = client.post("/api/promo/validate", json={"code": "save10", "amount": 2000})
        assert r.status_code == 200
        assert r.json()["valid"] is True

    def test_validate_empty_code(self, client):
        r = client.post("/api/promo/validate", json={"code": "", "amount": 1000})
        assert r.status_code == 200
        assert r.json()["valid"] is False

    def test_validate_message_included(self, client):
        r = client.post("/api/promo/validate", json={"code": "FLAT500", "amount": 2000})
        assert "message" in r.json()
        assert len(r.json()["message"]) > 0
