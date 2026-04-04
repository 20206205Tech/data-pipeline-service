from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.workflows import service
from common.response.base_response import BaseResponse
from database.config import get_db
from utils.log_function import log_function

router = APIRouter(
    prefix="/workflows", tags=["workflows"], dependencies=[Depends(require_admin)]
)


@router.get("", response_model=BaseResponse[Any])
@log_function
def list_workflows(db: Session = Depends(get_db)):
    """
    Danh sách các workflow đang có trong hệ thống
    """
    data = service.get_all_workflows(db)
    return BaseResponse(
        success=True, message="Lấy danh sách workflows thành công", data=data
    )


@router.get("/summary", response_model=BaseResponse[Any])
@log_function
def get_pipeline_summary(db: Session = Depends(get_db)):
    """
    Lấy thông tin tóm tắt pipeline
    """
    data = service.get_pipeline_summary(db)
    return BaseResponse(
        success=True, message="Lấy tóm tắt pipeline thành công", data=data
    )
