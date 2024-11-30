from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_document():
    """
    Placeholder endpoint for document-related functionality.
    """
    return {"message": "Document API is working!"}
