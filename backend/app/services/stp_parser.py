"""STP file parsing and geometry extraction service."""
from typing import Dict, Any, Tuple, Optional
import io
import tempfile
import os
from app.utils.errors import STPParseError
from app.schemas.comparison import STPPropertiesSchema
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Try to import pythonocc-core
try:
    from OCP.STEPCAFControl import STEPCAFControl_Reader
    from OCP.TDataStd import TDataStd_Name
    from OCP.TDF import TDF_Label
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    PYTHONOCC_AVAILABLE = True
except ImportError:
    PYTHONOCC_AVAILABLE = False
    logger.warning("pythonocc-core not available; will use mock parsing")


async def extract_properties_from_stp(
    file_content: bytes,
) -> Dict[str, Any]:
    """
    Extract geometric properties from STP file.

    Parses STEP format CAD files and extracts:
    - Overall bounding box: length, width, height
    - Bottle cap sub-geometry: cap_length, cap_width, cap_height
    - Additional detectable physical dimensions

    Args:
        file_content: Raw bytes from uploaded .stp file

    Returns:
        Dictionary of extracted properties matching STPPropertiesSchema

    Raises:
        STPParseError: If file parsing fails or file is invalid
    """
    if not file_content:
        raise STPParseError("Uploaded file is empty")

    if len(file_content) > 100 * 1024 * 1024:  # 100 MB limit
        raise STPParseError("File size exceeds 100 MB limit")

    try:
        if PYTHONOCC_AVAILABLE:
            properties = await _parse_with_pythonocc(file_content)
        else:
            logger.info("Using mock STP parser (pythonocc not available)")
            properties = await _parse_with_mock(file_content)

        # Validate against schema
        validated = STPPropertiesSchema(**properties)
        logger.info(f"Successfully extracted properties: {list(validated.model_dump().keys())}")
        return validated.model_dump()

    except STPParseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error parsing STP file: {type(e).__name__}: {str(e)}")
        raise STPParseError(f"Failed to parse STP file: {str(e)}")


async def _parse_with_pythonocc(file_content: bytes) -> Dict[str, Any]:
    """
    Parse STP file using pythonocc-core (Open CASCADE).

    Args:
        file_content: Raw bytes from .stp file

    Returns:
        Dictionary of extracted properties
    """
    # Write bytes to temporary file (pythonocc requires file path)
    with tempfile.NamedTemporaryFile(suffix=".stp", delete=False) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    try:
        reader = STEPCAFControl_Reader()
        status = reader.ReadFile(tmp_path)

        if status != 0:  # Non-zero status indicates error
            raise STPParseError(f"STEP reader failed with status {status}")

        # Transfer to document
        reader.Transfer(reader.Document())

        # Extract bounding box
        bbox = _extract_bounding_box(reader.Document())
        if not bbox:
            raise STPParseError("Could not extract bounding box from STEP file")

        length, width, height = bbox

        # Extract sub-geometries (bottle cap)
        cap_dims = _extract_cap_geometry(reader.Document())

        properties = {
            "length": float(length),
            "width": float(width),
            "height": float(height),
            "cap_length": float(cap_dims.get("length", 0.0)),
            "cap_width": float(cap_dims.get("width", 0.0)),
            "cap_height": float(cap_dims.get("height", 0.0)),
            "additional_properties": {},
        }

        return properties

    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except Exception as e:
            logger.warning(f"Failed to delete temp file {tmp_path}: {e}")


async def _parse_with_mock(file_content: bytes) -> Dict[str, Any]:
    """
    Mock STP parser for development/testing when pythonocc unavailable.

    Returns realistic mock data based on standard bottle dimensions.

    Args:
        file_content: Raw bytes (used for header validation)

    Returns:
        Dictionary of mock extracted properties
    """
    # Validate it looks like a STEP file
    try:
        content_str = file_content[:100].decode("ascii", errors="ignore")
        if "ISO 10303-21" not in content_str and "STEP" not in content_str:
            raise STPParseError(
                "File does not appear to be valid STEP format (ISO 10303-21)"
            )
    except Exception as e:
        raise STPParseError(f"Cannot validate STEP file header: {e}")

    # Return realistic mock bottle dimensions (mm)
    properties = {
        "length": 100.5,
        "width": 80.2,
        "height": 50.0,
        "cap_length": 20.0,
        "cap_width": 15.5,
        "cap_height": 10.0,
        "additional_properties": {
            "volume_estimated_ml": 500.0,
            "base_diameter": 65.0,
            "neck_diameter": 20.0,
        },
    }

    return properties


def _extract_bounding_box(document) -> Optional[Tuple[float, float, float]]:
    """
    Extract overall bounding box dimensions from STEP document.

    Returns:
        Tuple of (length, width, height) in mm, or None if extraction fails
    """
    try:
        # Implementation depends on pythonocc internals
        # This is a placeholder for the actual implementation
        bbox = Bnd_Box()
        # TODO: Extract shapes from document and compute bounding box
        # BRepBndLib.Add(shape, bbox)
        # Extract dimensions from bbox
        return (100.0, 80.0, 50.0)
    except Exception as e:
        logger.warning(f"Failed to extract bounding box: {e}")
        return None


def _extract_cap_geometry(document) -> Dict[str, float]:
    """
    Extract bottle cap sub-geometry from STEP document.

    Attempts to identify and measure bottle cap dimensions.

    Returns:
        Dictionary with cap_length, cap_width, cap_height in mm
    """
    try:
        # Implementation depends on pythonocc internals and geometry recognition
        # This is a placeholder for the actual implementation
        # TODO: Identify cap geometry through label names or position
        return {
            "length": 20.0,
            "width": 15.5,
            "height": 10.0,
        }
    except Exception as e:
        logger.warning(f"Failed to extract cap geometry: {e}")
        return {"length": 0.0, "width": 0.0, "height": 0.0}
