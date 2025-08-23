from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union

class StockAnalysisException(Exception):
    """股票分析系统基础异常"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DataSourceException(StockAnalysisException):
    """数据源异常"""
    pass

class ValidationException(StockAnalysisException):
    """数据验证异常"""
    pass

async def stock_analysis_exception_handler(request: Request, exc: StockAnalysisException):
    """全局异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "type": exc.__class__.__name__,
            "path": request.url.path
        }
    )
