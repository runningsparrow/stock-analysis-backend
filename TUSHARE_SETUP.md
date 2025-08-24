# Tushare 设置和使用指南

## 🚀 快速开始

### 1. 获取 Tushare Token

1. 访问 [Tushare官网](https://tushare.pro/)
2. 注册免费账号
3. 登录后在个人中心获取你的 API token

### 2. 配置环境变量

#### 方法1: 使用 .env 文件（推荐）

1. 将 `env.example` 重命名为 `.env`
2. 编辑 `.env` 文件，填入你的真实 token：

```bash
# 数据库配置
DB_DRIVER=mysql+pymysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=stock_analysis
DB_USER=stock_user
DB_PASSWORD=your_password_here

# Tushare API配置
TU_SHARE_TOKEN=your_actual_tushare_token_here

# 其他配置...
```

#### 方法2: 设置系统环境变量

```bash
# Windows PowerShell
$env:TU_SHARE_TOKEN="your_actual_tushare_token_here"

# Windows CMD
set TU_SHARE_TOKEN=your_actual_tushare_token_here

# Linux/Mac
export TU_SHARE_TOKEN="your_actual_tushare_token_here"
```

### 3. 在代码中使用

#### 基本用法

```python
from app.infrastructure.data.sources import TushareDataSource

# 创建实例
ts_source = TushareDataSource(token="your_token")

# 测试连接
is_connected = await ts_source.test_connection()
if is_connected:
    print("✅ Tushare连接成功！")
else:
    print("❌ Tushare连接失败")
```

#### 从配置文件获取 token

```python
from app.infrastructure.data.sources import TushareDataSource
from app.core.config import settings

# 从配置获取 token
token = settings.TU_SHARE_TOKEN
if token:
    ts_source = TushareDataSource(token=token)
else:
    print("请在 .env 文件中设置 TU_SHARE_TOKEN")
```

#### 完整示例

```python
import asyncio
from app.infrastructure.data.sources import TushareDataSource

async def main():
    # 创建 Tushare 数据源
    ts_source = TushareDataSource(token="your_token")
    
    # 测试连接
    if await ts_source.test_connection():
        print("连接成功！")
        
        # 获取股票基本信息
        stocks = await ts_source.get_stock_basic(exchange='SSE', list_status='L')
        print(f"获取到 {len(stocks)} 只股票")
        
        # 获取行情数据
        quote = await ts_source.get_stock_quote('000001.SZ')
        if quote:
            print(f"平安银行行情: {quote}")
    else:
        print("连接失败，请检查 token")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 测试连接

运行测试脚本验证配置：

```bash
# 测试所有数据源
python test_data_sources.py

# 测试 Tushare 特定功能
python example_tushare_usage.py
```

## 📊 可用功能

### 股票基本信息
```python
# 获取上交所股票
stocks = await ts_source.get_stock_basic(exchange='SSE', list_status='L')

# 获取深交所股票
stocks = await ts_source.get_stock_basic(exchange='SZSE', list_status='L')
```

### 行情数据
```python
# 获取指定日期行情
quote = await ts_source.get_stock_quote('000001.SZ', '20241201')

# 获取实时行情
realtime = await ts_source.get_stock_realtime_quote('000001.SZ')
```

### K线数据
```python
# 获取日线数据
daily = await ts_source.get_stock_kline('000001.SZ', 'daily')

# 获取周线数据
weekly = await ts_source.get_stock_kline('000001.SZ', 'weekly')

# 获取月线数据
monthly = await ts_source.get_stock_kline('000001.SZ', 'monthly')
```

### 财务数据
```python
# 获取年报数据
financial = await ts_source.get_stock_financial('000001.SZ', '20231231')
```

## ⚠️ 注意事项

1. **Token 安全**: 不要将真实的 token 提交到代码仓库
2. **API 限制**: 免费账号有 API 调用次数限制
3. **网络环境**: 确保网络环境能够访问 Tushare 服务
4. **错误处理**: 建议在生产环境中添加完善的异常处理

## 🆘 常见问题

### Q: 连接失败怎么办？
A: 检查以下几点：
- Token 是否正确
- 网络是否正常
- 是否超过了 API 调用限制

### Q: 如何获取更多数据？
A: 可以升级到付费账号，获得更高的 API 调用限制和更多数据

### Q: 数据格式不一致怎么办？
A: 两个数据源的数据格式略有不同，使用时需要注意字段映射

## 📚 更多资源

- [Tushare 官方文档](https://tushare.pro/document/1)
- [Tushare Python SDK](https://github.com/waditu/tushare)
- [项目数据源说明](DATA_SOURCES_README.md)
