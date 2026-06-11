"""API endpoints for session history and persistence."""
from fastapi import APIRouter, HTTPException
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/sessions", tags=["sessions"])

# Mock session storage (in production, use database)
SESSION_STORE = {}


@router.get("/")
async def list_sessions(limit: int = 10, offset: int = 0):
    """
    List user''s comparison sessions.

    Query Parameters:
        limit: Number of results per page
        offset: Number of results to skip

    Returns:
        Paginated list of sessions
    """
    sessions = list(SESSION_STORE.values())
    total = len(sessions)

    # Sort by date descending
    sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    # Paginate
    paginated = sessions[offset : offset + limit]

    logger.info(f"Listed {len(paginated)} of {total} sessions")
    return {
        "sessions": paginated,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{session_id}")
async def get_session(session_id: str):
    """Retrieve a specific comparison session by ID."""
    session = SESSION_STORE.get(session_id)

    if not session:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")

    logger.info(f"Retrieved session: {session_id}")
    return session


@router.post("/{session_id}/save")
async def save_session(session_id: str, data: dict):
    """Save or update a comparison session."""
    try:
        SESSION_STORE[session_id] = {
            **data,
            "session_id": session_id,
        }
        logger.info(f"Saved session: {session_id}")
        return {"session_id": session_id, "saved": True}
    except Exception as e:
        logger.error(f"Failed to save session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Delete a comparison session."""
    if session_id not in SESSION_STORE:
        raise HTTPException(status_code=404, detail="Session not found")

    del SESSION_STORE[session_id]
    logger.info(f"Deleted session: {session_id}")
    return {"session_id": session_id, "deleted": True}
