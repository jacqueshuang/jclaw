# Jclaw MVP

## 项目结构
- `apps/backend`：FastAPI + SQLAlchemy + Celery 后端
- `apps/desktop`：Vite + Vue 3 桌面前端
- `apps/desktop/src-tauri`：Tauri 2 + Rust 桌面壳
- `docker-compose.yml`：本地 PostgreSQL / Redis 依赖

## 环境要求
- Python 3.12+
- Node.js 20+
- npm 10+
- Rust stable
- Cargo
- Docker / Docker Compose

## 配置
1. 复制环境变量模板：
   - `cp .env.example .env`
2. 按需填写 `.env`：
   - `POSTGRES_DSN`：PostgreSQL 连接串
   - `REDIS_URL`：Redis 连接串
   - `APP_ENV`：运行环境，默认 `development`
   - `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY`：模型提供方密钥
   - `DEFAULT_MODEL_PROVIDER` / `DEFAULT_MODEL_NAME`：默认模型配置

## 依赖安装
### 后端
```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test,providers]"
```

### 前端
```bash
cd apps/desktop
npm install
```

### 桌面壳
```bash
cd apps/desktop/src-tauri
cargo test
```

## 本地运行
### 1. 启动基础依赖
```bash
docker compose up -d
```

### 2. 启动后端 API
```bash
cd apps/backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

默认地址：`http://127.0.0.1:8000`

### 3. 启动前端开发服务
```bash
cd apps/desktop
npm run dev
```

默认地址：`http://127.0.0.1:5173`

### 4. 启动桌面应用
```bash
cd apps/desktop/src-tauri
cargo tauri dev
```

当前 Rust 侧后端启动命令定义在 `apps/desktop/src-tauri/src/backend.rs`，默认通过：
```bash
python -m uvicorn app.main:app
```
启动后端。

## 测试与验证
## Verification targets
- `docker compose up -d`
- `make backend-test`
- `make desktop-test`
- `make lint`
- `make test`

也可以分别执行：

### 后端测试
```bash
cd apps/backend
source .venv/bin/activate
python -m pytest
```

### 前端测试
```bash
cd apps/desktop
npm test
```

### Rust 测试
```bash
cd apps/desktop/src-tauri
cargo test
```

## 部署说明
当前仓库是 MVP 形态，部署建议按“后端服务 + 桌面应用构建”拆开处理。

### 后端部署
建议最小部署形态：
- 1 个 FastAPI API 进程
- 1 个 Celery worker 进程
- 1 个 PostgreSQL
- 1 个 Redis

后端启动示例：
```bash
cd apps/backend
source .venv/bin/activate
pip install -e ".[test,providers]"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Celery worker 启动示例：
```bash
cd apps/backend
source .venv/bin/activate
pip install -e ".[test,providers]"
celery -A app.jobs.celery_app.celery_app worker --loglevel=info
```

部署前至少确认：
- `.env` 已配置生产数据库与 Redis
- 模型 API Key 已写入环境变量
- PostgreSQL / Redis 对后端服务可达
- 先执行过测试

### 桌面端构建
```bash
cd apps/desktop
npm install
npm run build
cd src-tauri
cargo tauri build
```

构建产物会由 Tauri 输出到其默认构建目录。

## Smoke expectation
- `make backend-test` should pass.
- `make desktop-test` should pass.
