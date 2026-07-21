import logging
from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from content import get_content_store
from content.store import ContentConflictError, ContentNotFoundError

router = APIRouter()
logger = logging.getLogger(__name__)

# Predefined list of editable JSON files for security validation
VALID_FILENAMES = {
    "ael.json",
    "be.json",
    "cil.json",
    "dc.json",
    "index.json",
    "rf.json",
    "sho.json"
}

def validate_filename(filename: str) -> None:
    if filename not in VALID_FILENAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid filename. Allowed files are: {', '.join(sorted(VALID_FILENAMES))}"
        )

@router.get("/content")
async def list_content_files():
    """Returns the list of editable content files, matching legacy /api/files format."""
    return [{"name": name} for name in sorted(VALID_FILENAMES)]

@router.get("/content/{filename}")
async def get_content(filename: str):
    """Fetches JSON content for a file, returning it directly with SHA in ETag/X-Content-SHA headers."""
    validate_filename(filename)
    store = get_content_store()
    try:
        content, sha = store.read(filename)
        headers = {
            "ETag": f'"{sha}"',
            "X-Content-SHA": sha,
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
        return JSONResponse(content=content, headers=headers)
    except ContentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/content/{filename}")
async def update_content(
    filename: str,
    request: Request,
    if_match: Optional[str] = Header(None),
    x_content_sha: Optional[str] = Header(None)
):
    """Updates JSON content for a file, validating concurrency version (SHA)."""
    validate_filename(filename)
    
    try:
        content = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON body")
        
    # Extract the client-provided SHA/version from headers
    sha = x_content_sha or if_match
    if sha:
        sha = sha.strip('"').strip("'")
        
    store = get_content_store()
    commit_message = f"Portal update for {filename}"
    
    try:
        new_sha = store.write(filename, content, sha=sha, message=commit_message)
        return {
            "success": True,
            "version": new_sha
        }
    except ContentConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error writing file {filename}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
