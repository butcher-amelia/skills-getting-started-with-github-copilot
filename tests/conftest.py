"""
Shared test fixtures for FastAPI backend tests.

Provides:
- TestClient instance for making HTTP requests
- Automatic state reset fixture to ensure deterministic tests
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state for restoration between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """
    Provide a TestClient instance for making HTTP requests to the app.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset the activities state before and after each test.

    This fixture is autouse=True, so it runs for every test and ensures
    that test state changes (like adding participants) do not leak into
    subsequent tests, making all tests deterministic.
    """
    # Arrange: Restore activities to original state before test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))

    # Test runs here
    yield

    # Cleanup: Restore activities to original state after test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
