import akshare as ak
from typing import Dict, Any, Optional

class TushareDataSource:
    """Tushare数据源适配器"""
    
    def __init__(self):
        self.token = None  # 从配置中获取
    
    async def get_stock_basic(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取股票基本信息"""
        try:
            # 使用akshare获取股票信息
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            return stock_info.to_dict('records')[0] if not stock_info.empty else None
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return None
    
    async def get_stock_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取股票价格信息"""
        try:
            # 获取实时价格
            price_info = ak.stock_zh_a_spot_em()
            stock_data = price_info[price_info['代码'] == symbol]
            return stock_data.to_dict('records')[0] if not stock_data.empty else None
        except Exception as e:
            print(f"获取股票价格失败: {e}")
            return None
