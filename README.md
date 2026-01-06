# SQLAlchemy FastAPI Demo

基于 [SQLAlchemy 官方文档快速入门](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) 创建的 FastAPI 示例项目。

## 项目结构

```
.
├── requirements.txt      # 项目依赖
├── database.py          # 数据库配置和模型定义
├── schemas.py           # Pydantic 数据验证模型
├── main.py              # FastAPI 应用和路由
└── test.db              # SQLite 数据库文件（自动创建）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python main.py
```

或者使用 uvicorn 直接运行：

```bash
uvicorn main:app --reload
```

应用将在 `http://localhost:8000` 启动。

### 3. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 核心概念

### 数据库模型

项目使用 SQLAlchemy 2.0 的新型映射方式，定义了两个模型：

#### User（用户）
- `id`: 主键
- `name`: 用户名（必填）
- `fullname`: 全名（可选）
- `addresses`: 关联的地址列表（一对多关系）

#### Address（地址）
- `id`: 主键
- `email_address`: 电子邮件地址
- `user_id`: 外键，引用用户
- `user`: 关联的用户对象（多对一关系）

### 关键 SQLAlchemy 特性

1. **DeclarativeBase** - 声明式基类，用于定义 ORM 模型
2. **Mapped** - 类型注解，用于声明列
3. **mapped_column()** - 列配置，用于指定列属性
4. **relationship()** - 关系配置，定义对象间关系
5. **Session** - 数据库会话，用于执行 CRUD 操作

## API 接口

### 用户接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/users/` | 创建新用户 |
| GET | `/users/` | 获取所有用户 |
| GET | `/users/{user_id}` | 获取指定用户 |
| PUT | `/users/{user_id}` | 更新用户信息 |
| DELETE | `/users/{user_id}` | 删除用户 |

### 地址接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/users/{user_id}/addresses/` | 创建地址 |
| GET | `/users/{user_id}/addresses/` | 获取用户的所有地址 |
| GET | `/addresses/{address_id}` | 获取指定地址 |
| DELETE | `/addresses/{address_id}` | 删除地址 |

## 使用示例

### 创建用户

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "spongebob", "fullname": "Spongebob Squarepants"}'
```

### 获取所有用户

```bash
curl "http://localhost:8000/users/"
```

### 为用户添加地址

```bash
curl -X POST "http://localhost:8000/users/1/addresses/" \
  -H "Content-Type: application/json" \
  -d '{"email_address": "spongebob@example.com"}'
```

## 技术栈

- **FastAPI** - 现代 Python Web 框架
- **SQLAlchemy** - Python ORM 和数据库工具包
- **Pydantic** - 数据验证库
- **SQLite** - 轻量级数据库（开发环境）
- **Uvicorn** - ASGI 服务器

## 学习资源

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/en/20/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM 快速入门](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
