# Jclaw MVP

## 项目结构
- `apps/backend`：FastAPI + SQLAlchemy + Celery 后端
- `apps/desktop`：OpenClaw Console 桌面前端（Vite + Vue 3）
- `apps/desktop/src-tauri`：OpenClaw Console 桌面壳（Tauri 2 + Rust）
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

### 2. 启动后端 API（可选）
```bash
cd apps/backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

默认地址：`http://127.0.0.1:8000`

### 3. 启动桌面应用
```bash
cd apps/desktop
npm run tauri:dev
```

桌面应用启动后会先检测 OpenClaw 是否已安装：
- 未安装：首页主按钮显示“安装”
- 已安装：首页主按钮显示“已安装”

当前首版控制台包含四个一级模块：
- 安装
- Skills
- Channel
- Agent

安装路径支持两种方向：
- 在线安装：已接通桌面端安装入口与状态流转
- 离线安装：已预留桌面端离线安装入口，离线包选择流程将在后续接入

## 测试与验证
桌面端当前验证闭环：

```bash
npm --prefix apps/desktop install
npm --prefix apps/desktop test
cargo test --manifest-path apps/desktop/src-tauri/Cargo.toml
npm --prefix apps/desktop run build
npm --prefix apps/desktop run tauri:build
```

期望结果：
- Vitest 通过
- Rust 测试通过
- Vite build 成功
- Tauri build 成功并产出桌面 bundle

如需分别执行：

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

### 桌面端构建验证
```bash
cd apps/desktop
npm run build
npm run tauri:build
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
python -m celery -A app.jobs.celery_app.celery_app worker --loglevel=info
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
npm run tauri:build
```

当前 macOS 默认产物为：
- `apps/desktop/src-tauri/target/release/bundle/macos/jclaw-desktop.app`

构建时会先自动执行前端构建，再由 Tauri 产出桌面应用包。

## Smoke expectation
- `make backend-test` should pass.
- `make desktop-test` should pass.
