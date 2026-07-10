from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_user, User
from database import get_database_session
import schemas

router = APIRouter(prefix="/context", tags=["Chats Management"])


def store_context(context: schemas.JenkinsContext) -> bool:
    return True

@router.post(
    "/{chat_id}/",
    response_model=schemas.ContextResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_context(
    payload: schemas.UploadContext,
    db_session: AsyncSession = Depends(get_database_session),
    current_user: User = Depends(get_current_user)
):
    print(payload.model_dump())
    store_context(payload.jenkins_context)
    
    return schemas.ContextResponse(success=True, received_data=payload.jenkins_context)
