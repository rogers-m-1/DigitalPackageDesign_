"""Tests for comparison logic service."""
import pytest
from app.services.comparison import calculate_property_deltas
from app.schemas.comparison import PropertyDelta


def test_calculate_property_deltas():
    """Test calculation of property deltas."""
    uploaded = {
        "length": 105.0,
        "width": 82.0,
        "height": 52.0,
        "cap_length": 21.0,
        "cap_width": 16.0,
        "cap_height": 11.0,
    }

    reference = {
        "length": 100.0,
        "width": 80.0,
        "height": 50.0,
        "cap_length": 20.0,
        "cap_width": 15.0,
        "cap_height": 10.0,
    }

    deltas = calculate_property_deltas(uploaded, reference)

    assert len(deltas) == 6
    assert all(isinstance(d, PropertyDelta) for d in deltas)

    # Check specific deltas
    length_delta = next((d for d in deltas if d.property_name == "length"), None)
    assert length_delta is not None
    assert length_delta.delta == 5.0
    assert length_delta.uploaded_value == 105.0
    assert length_delta.reference_value == 100.0


def test_calculate_property_deltas_negative():
    """Test negative deltas (uploaded smaller than reference)."""
    uploaded = {
        "length": 95.0,
        "width": 78.0,
        "height": 48.0,
        "cap_length": 19.0,
        "cap_width": 14.0,
        "cap_height": 9.0,
    }

    reference = {
        "length": 100.0,
        "width": 80.0,
        "height": 50.0,
        "cap_length": 20.0,
        "cap_width": 15.0,
        "cap_height": 10.0,
    }

    deltas = calculate_property_deltas(uploaded, reference)

    length_delta = next((d for d in deltas if d.property_name == "length"), None)
    assert length_delta.delta == -5.0


def test_calculate_property_deltas_missing_values():
    """Test handling of missing property values."""
    uploaded = {
        "length": 100.0,
        "width": 80.0,
    }

    reference = {
        "length": 100.0,
        "width": 80.0,
        "height": 50.0,
        "cap_length": 20.0,
        "cap_width": 15.0,
        "cap_height": 10.0,
    }

    deltas = calculate_property_deltas(uploaded, reference)

    height_delta = next((d for d in deltas if d.property_name == "height"), None)
    assert height_delta is not None
    assert height_delta.uploaded_value == 0.0  # Missing defaults to 0
    assert height_delta.delta == -50.0
