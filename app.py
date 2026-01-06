from fastapi import FastAPI, Request

from entity.database import create_tables
from common.router import APIRouterPro, auto_register_routers

# 创建FastAPI应用
app = FastAPI(title="SQLAlchemy FastAPI Demo - 模块化架构")


# 全局异常处理器 - 处理 Pydantic 验证错误
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    from pydantic import ValidationError
    if isinstance(exc, ValidationError):
        return {
            "status_code": 422,
            "detail": "输入数据验证失败",
            "errors": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        }
    return {"status_code": 500, "detail": "服务器内部错误"}


# 启动事件 - 创建数据库表
@app.on_event("startup")
def startup_event():
    create_tables()
    print("✅ 数据库表已创建")


# 使用自动路由注册功能
# 自动注册所有路由
auto_register_routers(app)


# ============ 根路由 ============

@app.get("/")
def root():
    """根路由 - 应用信息"""
    return {
        "message": "欢迎使用 SQLAlchemy FastAPI Demo - 模块化架构",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
