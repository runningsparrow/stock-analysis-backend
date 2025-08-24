# 股票分析系统 (Stock Analysis System)

## 项目简介

这是一个基于FastAPI的股票分析系统后端，采用DDD（领域驱动设计）架构，提供股票数据获取、分析和API服务。

## 技术栈

- **Web框架**: FastAPI
- **数据库**: MySQL + SQLAlchemy
- **数据源**: akshare (Tushare数据)
- **架构模式**: DDD (领域驱动设计)
- **Python版本**: 3.8+

## 项目结构

```
stock-analysis-backend/
├── app/                    # 主应用代码
│   ├── api/               # API路由层
│   ├── core/              # 核心基础设施
│   ├── domain/            # 领域层（核心业务逻辑）
│   └── infrastructure/    # 基础设施层
├── data/                  # 数据存储目录
├── scripts/               # 运维脚本
├── tasks/                 # 定时任务
└── tests/                 # 测试代码
```

## 快速开始

### 1. 环境准备

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example .env

# 编辑配置文件
vim .env
```

**重要**: 如果你要使用Tushare数据源，请在 `.env` 文件中设置你的Tushare API token：

```bash
TU_SHARE_TOKEN=your_actual_tushare_token_here
```

你可以从 [Tushare官网](https://tushare.pro/) 申请免费账号获取token。

### 3. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8011
```

### 4. 访问API

- API文档: http://localhost:8011/docs
- ReDoc文档: http://localhost:8011/redoc
- 健康检查: http://localhost:8011/health

## API接口

### 股票相关接口

- `GET /api/v1/stocks` - 获取股票列表
- `GET /api/v1/stocks/{symbol}` - 获取单个股票信息
- `GET /api/v1/stocks/{symbol}/price` - 获取股票实时价格

## 开发指南

### 添加新的API接口

1. 在 `app/api/v1/` 目录下创建新的路由文件
2. 在 `app/domain/services/` 下实现业务逻辑
3. 在 `app/domain/models/schemas/` 下定义数据模型
4. 添加相应的测试用例

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/domain/test_stock_service.py
```

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t stock-analysis .

# 运行容器
docker run -p 8011:8011 stock-analysis
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目地址: [https://github.com/username/stock-analysis-backend]
