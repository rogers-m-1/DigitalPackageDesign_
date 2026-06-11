"""Tests for export functionality."""
import pytest
from app.services.export import generate_pdf_export, generate_csv_export
from app.schemas.comparison import PropertyDelta


def test_generate_pdf_export():
    """Test PDF generation."""
    properties = [
        PropertyDelta(
            property_name="length",
            uploaded_value=105.0,
            reference_value=100.0,
            delta=5.0,
            unit="mm",
        ),
        PropertyDelta(
            property_name="width",
            uploaded_value=82.0,
            reference_value=80.0,
            delta=2.0,
            unit="mm",
        ),
    ]

    pdf_content = generate_pdf_export(
        "Test Bottle",
        "Reference Bottle",
        properties,
    )

    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
    assert b"%PDF" in pdf_content


def test_generate_csv_export():
    """Test CSV generation."""
    properties = [
        PropertyDelta(
            property_name="length",
            uploaded_value=105.0,
            reference_value=100.0,
            delta=5.0,
            unit="mm",
        ),
        PropertyDelta(
            property_name="width",
            uploaded_value=82.0,
            reference_value=80.0,
            delta=2.0,
            unit="mm",
        ),
    ]

    csv_content = generate_csv_export(
        "Test Bottle",
        "Reference Bottle",
        properties,
    )

    assert isinstance(csv_content, bytes)
    assert len(csv_content) > 0

    csv_text = csv_content.decode("utf-8")
    assert "Test Bottle" in csv_text
    assert "Reference Bottle" in csv_text
    assert "length" in csv_text
    assert "width" in csv_text
    assert "+5.00" in csv_text  # Delta value
