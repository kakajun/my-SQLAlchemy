# SQLAlchemy FastAPI Demo

基于 [SQLAlchemy 官方文档快速入门](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) 创建的 FastAPI 示例项目。

## 项目结构

```
.
├── common/                    # 公共模块
│   ├── constant.py            # 常量定义（HTTP状态码等）
│   ├── router.py              # 路由配置
│   └── vo.py                  # 视图对象（响应模型）
├── control/                   # 控制器层
│   ├── user_controller.py     # 用户控制器
│   └── address_controller.py  # 地址控制器
├── dto/                       # 数据传输对象
│   └── schemas.py             # Pydantic 数据验证模型
├── entity/                    # 实体层
│   ├── database.py            # 数据库配置
│   └── models.py              # ORM 模型定义
├── exceptions/                # 异常处理模块
│   ├── exception.py           # 自定义异常类
│   └── handle.py              # 全局异常处理器
├── middlewares/               # 中间件模块
│   ├── trace_middleware/      # 链路追踪中间件
│   │   ├── ctx.py             # 链路追踪上下文
│   │   ├── middle.py          # 链路追踪中间件实现
│   │   └── span.py            # 链路跨度定义
│   ├── cors_middleware.py     # CORS中间件
│   ├── gzip_middleware.py     # GZIP压缩中间件
│   └── handle.py              # 中间件注册处理
├── service/                   # 服务层
│   ├── user_service.py        # 用户服务
│   └── address_service.py     # 地址服务
├── utils/                     # 工具模块
│   ├── log_util.py            # 日志工具（Loguru配置）
│   └── response_util.py       # 响应工具类
├── requirements.txt           # 项目依赖
├── app.py                     # FastAPI 应用入口
└── README.md                  # 项目说明
```

## 快速开始

### 1. 安装依赖


```bash
uv venv --python=3.12 .venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

### 2. 运行应用


```bash
uvicorn app:app --reload
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
| POST | `/addresses/users/{user_id}` | 为用户创建地址 |
| GET | `/addresses/users/{user_id}` | 获取用户的所有地址 |
| GET | `/addresses/{address_id}` | 获取指定地址 |
| DELETE | `/addresses/{address_id}` | 删除地址 |

## 响应格式

所有接口返回统一的响应格式，基于 `common/vo.py` 中定义的响应模型：

### DataResponseModel
```json
{
  "code": 200,
  "msg": "操作成功",
  "success": true,
  "time": "2023-01-01T00:00:00",
  "data": {}
}
```

### CrudResponseModel
```json
{
  "is_success": true,
  "message": "操作成功",
  "result": {}
}
```

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
curl -X POST "http://localhost:8000/addresses/users/1" \
  -H "Content-Type: application/json" \
  -d '{"email_address": "spongebob@example.com"}'
```

## 技术栈

- **FastAPI** - 现代 Python Web 框架
- **SQLAlchemy** - Python ORM 和数据库工具包
- **Pydantic** - 数据验证库
- **SQLite** - 轻量级数据库（开发环境）
- **Uvicorn** - ASGI 服务器

## 系统架构

### 分层设计

```
请求 → 中间件层 → 控制器层 → 服务层 → 数据访问层 → 数据库
       ↓
    异常处理（统一响应格式）
```

**各层职责：**
- **Middlewares**：请求前处理（CORS、GZIP、链路追踪）
- **Controllers**：HTTP请求解析和响应
- **Services**：业务逻辑实现
- **Entity**：数据模型和数据库操作
- **DTO**：数据验证（Pydantic）
- **Exceptions**：统一异常处理和响应格式转换
- **Utils**：日志、响应等通用工具
- **Common**：常量、路由管理、响应模型

## 架构点评

### 优势

1. **清晰的分层架构**
   - Middleware层：请求前处理
   - Controller层：处理HTTP请求和响应
   - Service层：封装业务逻辑
   - Entity层：数据模型定义
   - DTO层：数据传输对象验证
   - Exception层：统一异常处理
   - Utils层：日志和工具支持

2. **可维护性**
   - 业务逻辑与HTTP层分离，便于维护
   - 代码职责清晰，易于定位问题

3. **可测试性**
   - Service层可以独立测试
   - 业务逻辑不受HTTP层影响

4. **统一异常处理与响应格式**
   - 所有接口返回一致的响应结构
   - Pydantic验证错误被拦截转换为统一格式
   - 自定义异常统一处理
   - 提高前端处理响应的一致性

5. **遵循SOLID原则**
   - 单一职责原则：每层只负责特定功能
   - 开闭原则：易于扩展新功能

6. **AI辅助开发友好**
   - 分层架构便于AI模型精确定位修改位置
   - 每层职责明确，减少AI理解代码的复杂度
   - 模式化CRUD操作便于AI识别和应用修改

7. **完整的中间件支持**
   - CORS跨域配置
   - GZIP响应压缩
   - 链路追踪（分布式追踪）

8. **专业的日志与监控**
   - Loguru日志框架
   - 自动错误追踪
   - 链路追踪支持

### 不足

1. **复杂度增加**
   - 对于简单CRUD应用可能存在过度设计
   - 需要维护更多的文件和类

2. **学习成本**
   - 新团队成员需要理解分层架构
   - 增加了代码导航的复杂性

3. **性能开销**
   - 多层调用可能带来微小性能开销

4. **代码冗余**
   - 相似的CRUD操作在不同层重复实现

## 学习资源

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/en/20/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM 快速入门](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)