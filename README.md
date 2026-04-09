# 地图闯关游戏

一款基于Vue 3 + FastAPI + MySQL的地图闯关互动游戏，包含站点内容展示、选择题答题、成就系统、排行榜、抽奖功能和管理后台。

## 技术栈

- **前端**：Vue 3 + Vite + Vue Router
- **后端**：Python + FastAPI
- **数据库**：MySQL
- **认证**：JWT + bcrypt密码加密

## 功能特性

- ✅ 用户注册登录系统
- ✅ 地图站点导航
- ✅ 站点内容展示
- ✅ 选择题答题系统
- ✅ 成就系统
- ✅ 实时排行榜
- ✅ 抽奖系统
- ✅ 邮寄地址收集
- ✅ 响应式设计
- ✅ 管理后台系统
  - 站点管理（增删改查）
  - 问题管理（增删改查）
  - 奖品管理（增删改查）
  - 成就管理（增删改查）
  - 用户管理（增删改查）
  - 抽奖记录管理

## 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- MySQL 5.7+

### 安装步骤

1. **项目结构**

项目已部署在 `d:\game` 目录下：

```
d:\game\
├── frontend/           # 前端项目
├── backend/            # 后端项目
├── README.md           # 项目说明
└── sql/               # SQL脚本
```

2. **安装前端依赖**

```bash
cd frontend
npm install
```

3. **安装后端依赖**

```bash
cd ../backend
pip install -r requirements.txt
```

4. **配置数据库**

- 确保MySQL服务已启动
- 修改 `backend/.env` 文件中的数据库配置：

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=123456
DB_NAME=map_game
```

5. **启动服务**

- 启动后端服务：

```bash
cd backend
python app.py
```

- 启动前端服务：

```bash
cd ../frontend
npm run dev
```

6. **访问游戏**

打开浏览器访问：http://localhost:8080/

7. **访问管理后台**

打开浏览器访问：http://localhost:8080/admin

## 项目结构

```
map-game/
├── frontend/           # 前端项目
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── router/     # 路由配置
│   │   └── services/   # API服务
│   ├── package.json    # 前端依赖
│   └── vite.config.js  # Vite配置
├── backend/            # 后端项目
│   ├── app.py          # FastAPI应用主文件
│   ├── requirements.txt # Python依赖
│   ├── .env           # 环境变量配置
│   ├── controllers/    # 控制器层 - 处理HTTP请求
│   │   ├── auth_controller.py      # 认证控制器
│   │   ├── station_controller.py   # 站点控制器
│   │   ├── progress_controller.py  # 进度控制器
│   │   ├── achievement_controller.py # 成就控制器
│   │   ├── leaderboard_controller.py # 排行榜控制器
│   │   ├── lottery_controller.py  # 抽奖控制器
│   │   └── admin_controller.py   # 管理后台控制器
│   ├── services/       # 服务层 - 业务逻辑
│   │   ├── auth_service.py        # 认证服务
│   │   ├── station_service.py     # 站点服务
│   │   ├── progress_service.py    # 进度服务
│   │   ├── achievement_service.py # 成就服务
│   │   ├── leaderboard_service.py # 排行榜服务
│   │   ├── lottery_service.py    # 抽奖服务
│   │   └── admin_service.py      # 管理后台服务
│   ├── schemas/        # 数据模型 - Pydantic模型
│   │   ├── user.py              # 用户模型
│   │   ├── station.py           # 站点模型
│   │   ├── progress.py          # 进度模型
│   │   ├── achievement.py        # 成就模型
│   │   └── lottery.py           # 抽奖模型
│   ├── common/         # 通用工具
│   │   ├── database.py          # 数据库连接
│   │   └── jwt_utils.py         # JWT工具
│   └── routes/         # 路由配置
│       ├── auth.py              # 认证路由
│       ├── station.py           # 站点路由
│       ├── progress.py          # 进度路由
│       ├── achievement.py        # 成就路由
│       ├── leaderboard.py       # 排行榜路由
│       ├── lottery.py           # 抽奖路由
│       └── admin.py             # 管理后台路由
├── README.md           # 项目说明
└── sql/               # SQL脚本
    └── init.sql        # 数据库初始化脚本
```

## 数据库结构

- **users**：用户信息
- **stations**：站点信息
- **questions**：问题信息
- **user_progress**：用户进度
- **achievements**：成就信息
- **user_achievements**：用户成就
- **lottery**：抽奖信息
- **leaderboard**：排行榜信息

## 开发指南

### 前端开发

- 页面组件位于 `frontend/src/views/`
- API服务位于 `frontend/src/services/`
- 路由配置位于 `frontend/src/router/`

### 后端开发

后端采用分层架构设计：

#### 控制器层 (Controllers)
- 负责处理HTTP请求和响应
- 调用服务层处理业务逻辑
- 处理用户认证和权限验证
- 所有控制器位于 `backend/controllers/` 目录

#### 服务层 (Services)
- 包含核心业务逻辑
- 处理数据库操作
- 实现业务规则和验证
- 所有服务位于 `backend/services/` 目录

#### 数据模型 (Schemas)
- 使用Pydantic定义数据结构
- 提供数据验证和序列化
- 所有模型位于 `backend/schemas/` 目录

#### 通用工具 (Common)
- 数据库连接管理
- JWT认证工具
- 密码加密和验证
- 通用工具位于 `backend/common/` 目录

#### 路由配置 (Routes)
- 集中管理API路由
- 将控制器路由注册到主应用
- 所有路由配置位于 `backend/routes/` 目录

## 模块说明

### 认证模块 (Auth)
- 用户注册
- 用户登录
- 获取当前用户信息
- JWT令牌验证

### 站点模块 (Station)
- 获取所有站点
- 获取站点详情（包含问题）

### 进度模块 (Progress)
- 获取用户进度
- 提交答案
- 更新用户分数和完成站点数

### 成就模块 (Achievement)
- 检查成就条件
- 获取用户成就列表
- 自动解锁成就

### 排行榜模块 (Leaderboard)
- 获取排行榜数据
- 按分数排序
- 显示排名

### 抽奖模块 (Lottery)
- 执行抽奖操作
- 提交邮寄地址
- 导出中奖名单

### 管理后台模块 (Admin)
- 站点管理：创建、编辑、删除站点，设置站点位置和内容
- 问题管理：为站点添加、编辑、删除问题和选项
- 奖品管理：设置奖品级别、概率和描述
- 成就管理：创建和管理成就系统
- 用户管理：查看和管理用户信息
- 抽奖记录管理：查看和管理抽奖记录

## 部署说明

1. **构建前端**

```bash
cd frontend
npm run build
```

2. **部署后端**

使用 uvicorn 或 Gunicorn 部署 FastAPI 应用：

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000
```

3. **配置 Nginx**

将前端静态文件部署到 Nginx，并反向代理后端 API。

## 注意事项

- 生产环境中请修改 `SECRET_KEY` 为安全的随机字符串
- 生产环境中请配置 HTTPS
- 生产环境中请使用环境变量管理敏感信息
- 后端已采用模块化设计，便于维护和扩展

## 许可证

MIT License
