from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import env
from index_router import index_router
from lifespan.lifespan import lifespan
from middlewares.log_request_and_response_middleware import (
    LogRequestAndResponseMiddleware,
)
from utils.log_function import log_function

app = FastAPI(
    lifespan=lifespan,
    description=f"""
Bạn có thể đăng nhập qua Google bằng đường dẫn dưới đây:
* [Đăng nhập với Google](https://{env.SUPABASE_PROJECT_ID}.supabase.co/auth/v1/authorize?provider=google)
    """,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogRequestAndResponseMiddleware)


app.include_router(index_router, prefix="/api")


@app.get("/")
@log_function
def root():
    return {"message": "Hello World", "docs": "/docs"}


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=30001)


if __name__ == "__main__":
    main()
