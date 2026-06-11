"""Reference design library service."""
from typing import Dict, List, Any, Optional
from app.utils.errors import ValidationError
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Mock database for reference designs (in production, use actual DB)
REFERENCE_LIBRARY = {
    "ref-001": {
        "id": "ref-001",
        "name": "Standard 500ml Bottle",
        "properties": {
            "length": 100.0,
            "width": 80.0,
            "height": 50.0,
            "cap_length": 20.0,
            "cap_width": 15.0,
            "cap_height": 10.0,
        },
        "source": "csv",
        "created_at": "2026-06-01T10:00:00Z",
    },
    "ref-002": {
        "id": "ref-002",
        "name": "Wide Mouth Bottle",
        "properties": {
            "length": 110.0,
            "width": 90.0,
            "height": 55.0,
            "cap_length": 25.0,
            "cap_width": 20.0,
            "cap_height": 12.0,
        },
        "source": "csv",
        "created_at": "2026-06-02T10:00:00Z",
    },
}


async def get_reference_design(design_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a reference design by ID.

    Args:
        design_id: Unique identifier for reference design

    Returns:
        Design entry dict with properties, or None if not found
    """
    design = REFERENCE_LIBRARY.get(design_id)
    if design:
        logger.info(f"Retrieved reference design: {design_id}")
    else:
        logger.warning(f"Reference design not found: {design_id}")
    return design


async def list_reference_designs(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """
    List all reference designs with pagination.

    Args:
        limit: Maximum number of results
        offset: Number of results to skip

    Returns:
        Dictionary with designs list and total count
    """
    designs = list(REFERENCE_LIBRARY.values())
    total = len(designs)

    # Apply pagination
    paginated = designs[offset : offset + limit]

    logger.info(f"Listed {len(paginated)} of {total} reference designs")
    return {
        "designs": paginated,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


async def search_reference_designs(
    query: str, limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Search reference designs by name.

    Args:
        query: Search query (case-insensitive substring match)
        limit: Maximum results

    Returns:
        List of matching designs
    """
    query_lower = query.lower()
    results = [
        d
        for d in REFERENCE_LIBRARY.values()
        if query_lower in d["name"].lower()
    ]

    logger.info(f"Search for '{query}' returned {len(results)} results")
    return results[:limit]
