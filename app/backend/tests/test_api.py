import pytest
import uuid

BASE_URL = "http://test"

@pytest.mark.asyncio
async def test_read_root(client):
    response = await client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Classifieds Pro API"}

@pytest.mark.asyncio
async def test_accounts_crud(client):
    unique_email = f"test-{uuid.uuid4()}@example.com"
    account_data = {
        "email": unique_email,
        "wanuncios_password": "password123"
    }

    # --- CREATE ---
    response = await client.post("/api/accounts/", json=account_data)
    assert response.status_code == 200
    created_account = response.json()
    account_id = created_account["id"]

    # --- READ (one) ---
    response = await client.get(f"/api/accounts/{account_id}")
    assert response.status_code == 200
    assert response.json()["email"] == unique_email

    # --- DELETE ---
    response = await client.delete(f"/api/accounts/{account_id}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_ads_crud(client):
    # --- SETUP: Create an account ---
    unique_email = f"test-ad-{uuid.uuid4()}@example.com"
    account_data = {"email": unique_email, "wanuncios_password": "password"}
    response = await client.post("/api/accounts/", json=account_data)
    assert response.status_code == 200
    account_id = response.json()["id"]

    # --- CREATE AD ---
    ad_data = {
        "account_id": account_id,
        "title": "Test Ad",
        "description": "This is a test description.",
        "category": "Contactos",
        "subcategory": "Relaciones Ocasionales",
        "province": "Panamá"
    }
    response = await client.post("/api/ads/", json=ad_data)
    assert response.status_code == 200
    ad_id = response.json()["id"]

    # --- READ AD ---
    response = await client.get(f"/api/ads/{ad_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ad"

    # --- DELETE AD ---
    response = await client.delete(f"/api/ads/{ad_id}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_schedules_crud(client):
    # --- SETUP: Create account and ad ---
    unique_email = f"test-sched-{uuid.uuid4()}@example.com"
    account_data = {"email": unique_email, "wanuncios_password": "password"}
    res_acc = await client.post("/api/accounts/", json=account_data)
    account_id = res_acc.json()["id"]

    ad_data = { "account_id": account_id, "title": "Sched Test Ad", "description": "d", "category": "Contactos", "subcategory": "Relaciones Ocasionales", "province": "Panamá" }
    res_ad = await client.post("/api/ads/", json=ad_data)
    ad_id = res_ad.json()["id"]

    # --- CREATE SCHEDULE ---
    schedule_data = {
        "ad_id": ad_id,
        "republish_interval_hours": 12
    }
    response = await client.post("/api/schedules/", json=schedule_data)
    assert response.status_code == 200
    schedule_id = response.json()["id"]

    # --- READ SCHEDULE ---
    response = await client.get(f"/api/schedules/{schedule_id}")
    assert response.status_code == 200
    assert response.json()["republish_interval_hours"] == 12

    # --- DELETE SCHEDULE ---
    response = await client.delete(f"/api/schedules/{schedule_id}")
    assert response.status_code == 204
