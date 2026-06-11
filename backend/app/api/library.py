"""API endpoints for reference library operations."""
from fastapi import APIRouter, HTTPException, Query
from app.services.library import (
    get_reference_design,
    list_reference_designs,
    search_reference_designs,
)

router = APIRouter(prefix="/api/library", tags=["library"])


@router.get("/designs")
async def get_designs_list(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    """
    List all reference designs with pagination.

    Query Parameters:
        limit: Number of results per page (1-100, default 50)
        offset: Number of results to skip (default 0)

    Returns:
        Paginated list of reference designs
    """
    try:
        result = await list_reference_designs(limit=limit, offset=offset)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/designs/{design_id}")
async def get_design_detail(design_id: str):
    """
    Retrieve a specific reference design by ID.

    Path Parameters:
        design_id: Unique reference design identifier

    Returns:
        Design entry with all properties
    """
    design = await get_reference_design(design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design


@router.get("/search")
async def search_designs(q: str = Query(..., min_length=1), limit: int = Query(50, ge=1, le=100)):
    """
    Search reference designs by name.

    Query Parameters:
        q: Search query (required, minimum 1 character)
        limit: Maximum results (1-100, default 50)

    Returns:
        List of matching designs
    """
    try:
        results = await search_reference_designs(q, limit=limit)
        return {"query": q, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
