from fastapi import FastAPI
from utils.log_util import logger
from entity.database import create_tables
from common.router import auto_register_routers
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware

# 创建FastAPI应用
app = FastAPI(title="SQLAlchemy FastAPI Demo - 模块化架构")


# 启动事件 - 创建数据库表
@app.on_event("startup")
def startup_event():
    create_tables()
    print("✅ 数据库表已创建")
    print("🚀 http://127.0.0.1:8000/docs 开始启动")


# 统一异常处理
handle_exception(app)
# 自动注册所有路由
auto_register_routers(app)
# 加载中间件处理方法
handle_middleware(app)

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
