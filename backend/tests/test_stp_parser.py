"""Tests for STP file parsing service."""
import pytest
from app.services.stp_parser import extract_properties_from_stp
from app.utils.errors import STPParseError


@pytest.mark.asyncio
async def test_extract_properties_from_mock_stp():
    """Test extracting properties from mock STP file."""
    # Mock STP file header (ISO 10303-21 is STEP format signature)
    mock_stp_content = b"""ISO 10303-21;
HEADER;
FILE_DESCRIPTION(('Bottle design'),''2026-06-09T12:00:00'','');
FILE_NAME('bottle.stp','',(''),(''),'','','');
FILE_SCHEMA(('AP203_CONFIGURATION_CONTROLLED_3D_DESIGN_OF_MECHANICAL_PARTS_AND_ASSEMBLIES_MIM_LF',''));
ENDSEC;
DATA;
ENDSEC;
END-ISO-10303-21;"""

    properties = await extract_properties_from_stp(mock_stp_content)

    # Verify all required properties are present
    assert "length" in properties
    assert "width" in properties
    assert "height" in properties
    assert "cap_length" in properties
    assert "cap_width" in properties
    assert "cap_height" in properties

    # Verify they are numeric
    assert isinstance(properties["length"], (int, float))
    assert isinstance(properties["width"], (int, float))
    assert isinstance(properties["height"], (int, float))
    assert properties["length"] > 0
    assert properties["width"] > 0
    assert properties["height"] > 0


@pytest.mark.asyncio
async def test_extract_properties_empty_file():
    """Test that empty file raises STPParseError."""
    with pytest.raises(STPParseError):
        await extract_properties_from_stp(b"")


@pytest.mark.asyncio
async def test_extract_properties_invalid_format():
    """Test that invalid file format raises STPParseError."""
    invalid_content = b"This is not a STEP file at all"
    with pytest.raises(STPParseError):
        await extract_properties_from_stp(invalid_content)


@pytest.mark.asyncio
async def test_extract_properties_file_too_large():
    """Test that oversized file raises STPParseError."""
    huge_content = b"x" * (101 * 1024 * 1024)  # 101 MB
    with pytest.raises(STPParseError):
        await extract_properties_from_stp(huge_content)
