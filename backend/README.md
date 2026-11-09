# HFUT-PerceptPulse 后端服务 (Backend)

基于 **Python + FastAPI + SQLite + SQLAlchemy** 构建的轻量级校园学术与竞赛情报感知系统后端。

## 目录结构

- `app/`
  - `core/`: 数据库连接配置 (`database.py`) 与全局常量 (`config.py`)
  - `models/`: SQLAlchemy 数据模型 (`item.py` 包含 `PulseItem` 和 `CrawlSource`)
  - `schemas/`: Pydantic 数据输入输出契约与校验
  - `api/v1/`: RESTful API 路由 (`items.py` 获取/创建情报, `stats.py` 统计汇总)
  - `services/crawlers/`: 校园信息感知爬虫与清洗模块（后续阶段接入）
  - `main.py`: FastAPI 应用入口，配置了跨域 CORS 与生命周期
- `data/`: 存放本地 SQLite 单文件数据库 `pulse.db`
- `seed_data.py`: 初始化并填充工大代表性学术讲座与竞赛样本数据
- `tests/`: 接口自测脚本

## 本地启动与调试

### 1. 激活虚拟环境 (Windows PowerShell)
```powershell
.\backend\.venv\Scripts\Activate.ps1
```

### 2. 启动 FastAPI 本地开发服务器
在 `backend` 目录下执行：
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. 查看交互式 API 文档 (Swagger UI)
启动后，在浏览器访问：
- API 文档界面：http://127.0.0.1:8000/docs
- 备用文档界面：http://127.0.0.1:8000/redoc
- 系统健康检查：http://127.0.0.1:8000/
