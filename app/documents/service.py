from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session


def get_document_total(db: Session):
    """Lấy thông tin tổng số văn bản từ bản ghi mới nhất"""
    query = text(
        """
        SELECT total_count, update_at
        FROM document_total
        ORDER BY update_at DESC
        LIMIT 1
        """
    )
    try:
        row = db.execute(query).fetchone()
        if not row:
            return {"total_count": 0, "update_at": None}
        return {"total_count": row[0], "update_at": row[1]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi document_total: {str(e)}")


def get_document_status_report(db: Session):
    """Báo cáo số lượng văn bản phân loại theo trạng thái"""
    query = text(
        """
        SELECT
            status,
            COUNT(item_id) as total_count,
            MIN(update_at) as oldest_update,
            MAX(update_at) as latest_update
        FROM document_info
        GROUP BY status
        ORDER BY total_count DESC
        """
    )
    try:
        result = db.execute(query).fetchall()
        return [
            {
                "status": row[0],
                "count": row[1],
                "oldest_update": row[2],
                "latest_update": row[3],
            }
            for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi document_info: {str(e)}")


def get_recent_documents(db: Session, limit: int = 10):
    query = text(
        """
        SELECT ds.item_id, w.code, ds.end_time
        FROM document_state ds
        JOIN workflows w ON ds.workflow_id = w.id
        WHERE ds.end_time IS NOT NULL
        ORDER BY ds.end_time DESC
        LIMIT :limit
    """
    )
    try:
        result = db.execute(query, {"limit": limit}).fetchall()
        return [
            {"item_id": row[0], "step_code": row[1], "completed_at": row[2]}
            for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi recent_documents: {str(e)}")


def get_issue_date_report(db: Session):
    """Thống kê số lượng văn bản theo năm ban hành"""
    query = text(
        """
        SELECT
            EXTRACT(YEAR FROM issue_date)::INTEGER as issue_year,
            COUNT(item_id) as total_count
        FROM document_info
        WHERE issue_date IS NOT NULL
        GROUP BY issue_year
        ORDER BY issue_year DESC
    """
    )
    try:
        result = db.execute(query).fetchall()
        return [{"year": row[0], "count": row[1]} for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi issue_date_report: {str(e)}")
