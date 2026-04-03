from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.workflows import service
from database.config import get_db
from utils.log_function import log_function

router = APIRouter(prefix="/workflows", tags=["workflows"])


router = APIRouter(
    prefix="/workflows", tags=["workflows"], dependencies=[Depends(require_admin)]
)


@router.get("")
@log_function
def list_workflows(db: Session = Depends(get_db)):
    """
    Danh sách các workflow đang có trong hệ thống
    """
    return service.get_all_workflows(db)


@router.get("/summary")
@log_function
def get_pipeline_summary(db: Session = Depends(get_db)):
    """
    Lấy thông tin tóm tắt pipeline
    """
    return service.get_pipeline_summary(db)
