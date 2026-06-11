"""API endpoints for comparison operations."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional
import uuid
from datetime import datetime
from app.schemas.comparison import PropertyDelta
from app.services.stp_parser import extract_properties_from_stp
from app.services.comparison import calculate_property_deltas
from app.services.export import generate_pdf_export, generate_csv_export
from app.services.library import get_reference_design
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/comparisons", tags=["comparisons"])


@router.post("/upload-and-compare")
async def upload_and_compare(
    file: UploadFile = File(...),
    reference_design_id: Optional[str] = Form(None),
    reference_design_name: Optional[str] = Form(None),
):
    """
    Upload STP file, extract properties, and compare against reference design.

    Form Parameters:
        file: STP file (required)
        reference_design_id: ID of reference design to compare against
        reference_design_name: Name of reference design (for display)

    Returns:
        Comparison results with 3-column table data and session ID
    """
    # Validate file type
    if not file.filename.endswith(".stp"):
        raise HTTPException(status_code=400, detail="File must be .stp format")

    try:
        # Read file content
        file_content = await file.read()
        logger.info(f"Received file: {file.filename} ({len(file_content)} bytes)")

        # Extract properties from uploaded STP
        uploaded_properties = await extract_properties_from_stp(file_content)
        logger.info(f"Extracted properties: {list(uploaded_properties.keys())}")

        # Fetch reference properties
        if reference_design_id:
            reference = await get_reference_design(reference_design_id)
            if reference:
                reference_properties = reference.get("properties", {})
                reference_name = reference.get("name", "Reference Design")
            else:
                raise HTTPException(status_code=404, detail="Reference design not found")
        else:
            # Use mock reference if not specified
            reference_properties = {
                "length": 105.0,
                "width": 82.0,
                "height": 52.0,
                "cap_length": 21.0,
                "cap_width": 16.0,
                "cap_height": 11.0,
            }
            reference_name = reference_design_name or "Reference Design"

        # Calculate deltas
        deltas = calculate_property_deltas(uploaded_properties, reference_properties)
        logger.info(f"Calculated {len(deltas)} property deltas")

        session_id = str(uuid.uuid4())

        return {
            "session_id": session_id,
            "uploaded_design_name": file.filename,
            "reference_design_id": reference_design_id or "default",
            "reference_design_name": reference_name,
            "properties": [d.model_dump() for d in deltas],
            "timestamp": datetime.now().isoformat(),
            "message": "Comparison completed successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comparison failed: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.post("/export-pdf")
async def export_pdf(
    uploaded_name: str = Form(...),
    reference_name: str = Form(...),
    properties_json: str = Form(...),
):
    """
    Generate and download PDF export of comparison results.

    Form Parameters:
        uploaded_name: Name of uploaded design
        reference_name: Name of reference design
        properties_json: JSON array of PropertyDelta objects

    Returns:
        PDF file for download
    """
    try:
        import json
        properties_data = json.loads(properties_json)

        # Convert to PropertyDelta objects
        properties = [PropertyDelta(**p) for p in properties_data]

        pdf_content = generate_pdf_export(uploaded_name, reference_name, properties)

        return StreamingResponse(
            iter([pdf_content]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"},
        )

    except Exception as e:
        logger.error(f"PDF export failed: {e}")
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post("/export-csv")
async def export_csv(
    uploaded_name: str = Form(...),
    reference_name: str = Form(...),
    properties_json: str = Form(...),
):
    """
    Generate and download CSV export of comparison results.

    Form Parameters:
        uploaded_name: Name of uploaded design
        reference_name: Name of reference design
        properties_json: JSON array of PropertyDelta objects

    Returns:
        CSV file for download
    """
    try:
        import json
        properties_data = json.loads(properties_json)

        # Convert to PropertyDelta objects
        properties = [PropertyDelta(**p) for p in properties_data]

        csv_content = generate_csv_export(uploaded_name, reference_name, properties)

        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"},
        )

    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")


@router.get("/sessions/{session_id}")
async def get_comparison_session(session_id: str):
    """Retrieve a past comparison session."""
    # TODO: Fetch from database
    return {
        "session_id": session_id,
        "message": "Feature coming soon",
    }


@router.get("/sessions")
async def list_comparison_sessions(limit: int = 10, offset: int = 0):
    """List user''s past comparison sessions."""
    # TODO: Query database with pagination
    return {
        "sessions": [],
        "total": 0,
    }
