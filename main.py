from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

import env
from lifespan.lifespan import lifespan
from utils.log_function import log_function

DATABASE_URL = env.DATA_PIPELINE_VBPL_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@log_function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
@log_function
def root():
    return {"message": "Hello World", "docs": "/docs"}


@app.get("/workflows/list")
@log_function
def list_workflows(db: Session = Depends(get_db)):
    """
    Danh sách các workflow đang có trong hệ thống
    """
    query = text("SELECT id, code, description FROM workflows")
    result = db.execute(query).fetchall()
    return [{"id": r[0], "code": r[1], "description": r[2]} for r in result]


@app.get("/stats/summary")
@log_function
def get_pipeline_summary(db: Session = Depends(get_db)):
    """
    Thống kê số lượng văn bản đã hoàn thành theo từng loại workflow.
    Trả về: workflow_id, code và tổng số item.
    """
    query = text(
        """
        SELECT
            w.id as workflow_id,
            w.code,
            COUNT(ds.item_id) as total_items
        FROM document_state ds
        JOIN workflows w ON ds.workflow_id = w.id
        WHERE ds.end_time IS NOT NULL
        GROUP BY w.id, w.code
        ORDER BY w.id ASC
    """
    )
    try:
        result = db.execute(query).fetchall()

        return [
            {"workflow_id": row[0], "code": row[1], "total_items": row[2]}
            for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/recent")
@log_function
def get_recent_documents(limit: int = 10, db: Session = Depends(get_db)):
    """
    Lấy danh sách các văn bản vừa hoàn thành một bước nào đó gần đây nhất
    """
    query = text(
        f"""
        SELECT ds.item_id, w.code, ds.end_time
        FROM document_state ds
        JOIN workflows w ON ds.workflow_id = w.id
        WHERE ds.end_time IS NOT NULL
        ORDER BY ds.end_time DESC
        LIMIT {limit}
    """
    )
    result = db.execute(query).fetchall()
    return [
        {"item_id": row[0], "step_code": row[1], "completed_at": row[2]}
        for row in result
    ]


@app.get("/stats/document-status")
@log_function
def get_document_status_report(db: Session = Depends(get_db)):
    """
    Báo cáo số lượng văn bản phân loại theo trạng thái (status) từ bảng document_info
    """
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

        if not result:
            return []

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
        raise HTTPException(
            status_code=500, detail=f"Lỗi khi truy vấn bảng document_info: {str(e)}"
        )


@app.get("/stats/issue-date-report")
@log_function
def get_issue_date_report(db: Session = Depends(get_db)):
    """
    Thống kê số lượng văn bản theo năm ban hành (issue_date)
    """
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
        raise HTTPException(status_code=500, detail=str(e))


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
