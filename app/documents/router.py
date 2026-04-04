from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_admin
from app.documents import service
from database.config import get_db
from utils.log_function import log_function

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/total")
@log_function
def get_document_total(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Lấy thông tin tổng số văn bản"""
    return service.get_document_total(db)


@router.get("/status", dependencies=[Depends(require_admin)])
@log_function
def get_document_status_report(db: Session = Depends(get_db)):
    """Báo cáo trạng thái văn bản"""
    return service.get_document_status_report(db)


@router.get("/recent", dependencies=[Depends(require_admin)])
@log_function
def get_recent_documents(limit: int = 10, db: Session = Depends(get_db)):
    """Lấy danh sách gần đây"""
    return service.get_recent_documents(db, limit=limit)


@router.get("/issue-date", dependencies=[Depends(require_admin)])
@log_function
def get_issue_date_report(db: Session = Depends(get_db)):
    """Thống kê theo năm"""
    return service.get_issue_date_report(db)


@router.get("/info", dependencies=[Depends(require_admin)])
@log_function
def get_document_info(
    item_id: Optional[int] = None,
    document_number: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Lấy thông tin chi tiết của văn bản theo item_id hoặc document_number"""
    return service.get_document_info_detail(
        db, item_id=item_id, document_number=document_number
    )
