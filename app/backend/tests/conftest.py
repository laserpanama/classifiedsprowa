import pytest
import httpx
from asgi_lifespan import LifespanManager
from app.backend.main import app as main_app
from app.backend.api import accounts, ads, schedules
from motor.motor_asyncio import AsyncIOMotorDatabase
import mongomock_motor
import asyncio

# --- Mocking Services ---
@pytest.fixture(scope="session", autouse=True)
def mock_services(session_mocker):
    """Mocks services for the entire test session."""
    session_mocker.patch("app.backend.services.scheduler_service.initialize_scheduler", return_value=None)
    session_mocker.patch("app.backend.services.scheduler_service.shutdown_scheduler", return_value=None)
    session_mocker.patch("app.backend.api.schedules.sched_svc.schedule_ad_posting_job", return_value=None)
    session_mocker.patch("app.backend.api.schedules.sched_svc.remove_schedule", return_value=None)
    session_mocker.patch("app.backend.services.automation_service.post_ad_to_wanuncios", return_value=None)

# --- Mocking the Database ---
@pytest.fixture(scope="session")
def mock_db():
    """Provides a mock database for the test session."""
    return mongomock_motor.AsyncMongoMockClient().get_database("test_db")

@pytest.fixture(scope="session", autouse=True)
def override_db_dependency(mock_db):
    """Applies the database dependency override for the entire session."""
    async def override_get_database() -> AsyncIOMotorDatabase:
        return mock_db

    main_app.dependency_overrides[accounts.get_database] = override_get_database
    main_app.dependency_overrides[ads.get_database] = override_get_database
    main_app.dependency_overrides[schedules.get_database] = override_get_database
    yield
    main_app.dependency_overrides = {}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def client(anyio_backend):
    """
    An async client that can be used to make requests to the app.
    The LifespanManager ensures that startup and shutdown events are handled.
    """
    async with LifespanManager(main_app):
        transport = httpx.ASGITransport(app=main_app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
            yield c

@pytest.fixture(scope="function", autouse=True)
async def clear_collections(mock_db):
    """Clears all data from the mock database after each test."""
    yield
    for collection in await mock_db.list_collection_names():
        await mock_db[collection].delete_many({})
