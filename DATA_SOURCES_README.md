# 数据源使用说明

本项目支持两个数据源来获取股票数据：

## 1. Tushare数据源 (TushareDataSource)

### 特点
- **专业数据服务**: 提供高质量的金融数据
- **需要注册**: 需要申请Tushare账号和API token
- **数据全面**: 包含股票、基金、债券、期货等数据
- **稳定性高**: 专业的数据服务，稳定性较好

### 使用方法

#### 1.1 配置Token
在 `.env` 文件中添加：
```bash
TU_SHARE_TOKEN=your_tushare_token_here
```

#### 1.2 初始化数据源
```python
from app.infrastructure.data.sources import TushareDataSource

# 创建实例
ts_source = TushareDataSource(token="your_token")

# 测试连接
is_connected = await ts_source.test_connection()
```

#### 1.3 主要功能

##### 获取股票基本信息
```python
# 获取上交所上市股票
stocks = await ts_source.get_stock_basic(exchange='SSE', list_status='L')

# 获取深交所上市股票
stocks = await ts_source.get_stock_basic(exchange='SZSE', list_status='L')
```

##### 获取股票行情
```python
# 获取指定日期的行情
quote = await ts_source.get_stock_quote('000001.SZ', '20241201')

# 获取实时行情
realtime = await ts_source.get_stock_realtime_quote('000001.SZ')
```

##### 获取K线数据
```python
# 获取日线数据
daily_data = await ts_source.get_stock_kline('000001.SZ', 'daily')

# 获取周线数据
weekly_data = await ts_source.get_stock_kline('000001.SZ', 'weekly')

# 获取月线数据
monthly_data = await ts_source.get_stock_kline('000001.SZ', 'monthly')
```

##### 获取财务数据
```python
# 获取年报数据
financial = await ts_source.get_stock_financial('000001.SZ', '20231231')
```

## 2. 东方财富网数据源 (EastMoneyDataSource)

### 特点
- **免费使用**: 无需注册，直接使用
- **数据实时**: 提供实时行情数据
- **覆盖全面**: 覆盖A股、港股、美股等
- **基于akshare**: 使用akshare库获取数据

### 使用方法

#### 2.1 初始化数据源
```python
from app.infrastructure.data.sources import EastMoneyDataSource

# 创建实例
em_source = EastMoneyDataSource()

# 测试连接
is_connected = await em_source.test_connection()
```

#### 2.2 主要功能

##### 获取股票基本信息
```python
# 获取单个股票信息
stock_info = await em_source.get_stock_basic('000001')

# 获取所有A股信息
all_stocks = await em_source.get_stock_basic()
```

##### 获取实时行情
```python
# 获取单个股票实时行情
quote = await em_source.get_stock_realtime_quote('000001')

# 获取所有A股实时行情
all_quotes = await em_source.get_stock_realtime_quote()
```

## 3. 数据格式对比

### Tushare数据格式
```python
# 股票基本信息
{
    'ts_code': '000001.SZ',
    'symbol': '000001',
    'name': '平安银行',
    'area': '深圳',
    'industry': '银行',
    'market': '主板',
    'list_date': '19910403',
    'is_hs': 'N'
}

# 行情数据
{
    'ts_code': '000001.SZ',
    'trade_date': '20241201',
    'open': 12.50,
    'high': 12.80,
    'low': 12.30,
    'close': 12.60,
    'pre_close': 12.40,
    'change': 0.20,
    'pct_chg': 1.61,
    'vol': 1234567,
    'amount': 15555555.55
}
```

### 东方财富网数据格式
```python
# 股票基本信息
{
    'symbol': '000001',
    'name': '平安银行',
    'exchange': 'SZSE',
    'industry': '银行',
    'market_type': '主板',
    'listing_date': '1991-04-03',
    'total_shares': 19405918123,
    'circulating_shares': 19405918123,
    'pe_ratio': 5.23,
    'pb_ratio': 0.45,
    'market_cap': 244.5,
    'circulating_market_cap': 244.5
}

# 实时行情
{
    'symbol': '000001',
    'name': '平安银行',
    'current_price': 12.60,
    'change_amount': 0.20,
    'change_percent': 1.61,
    'open_price': 12.50,
    'high_price': 12.80,
    'low_price': 12.30,
    'prev_close': 12.40,
    'volume': 1234567,
    'amount': 15555555.55,
    'turnover_rate': 0.64,
    'pe_ratio': 5.23,
    'pb_ratio': 0.45,
    'market_cap': 244.5,
    'circulating_market_cap': 244.5,
    'quote_time': '2024-12-01 15:00:00'
}
```

## 4. 选择建议

### 使用Tushare的场景
- 需要高质量、稳定的数据
- 有Tushare账号和token
- 需要历史数据或财务数据
- 生产环境使用

### 使用东方财富网的场景
- 快速原型开发
- 测试环境使用
- 只需要实时行情数据
- 预算有限的情况

## 5. 测试数据源

运行测试脚本：
```bash
python test_data_sources.py
```

## 6. 注意事项

1. **Tushare限制**: 免费账号有API调用次数限制
2. **网络环境**: 东方财富网数据源需要稳定的网络环境
3. **数据一致性**: 两个数据源的数据格式略有不同，使用时需要注意
4. **异常处理**: 建议在生产环境中添加完善的异常处理机制

## 7. 扩展开发

如需添加新的数据源，可以：
1. 在 `app/infrastructure/data/sources/` 目录下创建新的数据源类
2. 实现统一的数据接口
3. 在 `__init__.py` 中导入新数据源
4. 添加相应的测试用例
