"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_stp_file():
    """Mock sample STP file for testing."""
    # TODO: Use actual fixture file from tests/fixtures/sample.stp
    return b"STEP file content mock"


@pytest.fixture
def sample_csv_data():
    """Mock CSV data for testing."""
    return b"""name,length,width,height,cap_length,cap_width,cap_height
Design_A,100.0,80.0,50.0,20.0,15.0,10.0
Design_B,110.0,85.0,55.0,21.0,16.0,11.0
"""
