from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import secrets

class Settings(BaseSettings):
    # 数据库配置
    DB_DRIVER: str = Field(default="mysql+pymysql", env="DB_DRIVER")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=3306, env="DB_PORT")
    DB_NAME: str = Field(default="stock_analysis", env="DB_NAME")
    DB_USER: str = Field(default="stock_user", env="DB_USER")
    DB_PASSWORD: str = Field(default="", env="DB_PASSWORD")
    DB_URL: Optional[str] = None
    
    # 数据源配置
    TU_SHARE_TOKEN: Optional[str] = Field(None, env="TU_SHARE_TOKEN")
    SINA_API_ENDPOINT: str = Field(default="https://hq.sinajs.cn/list=", env="SINA_API_ENDPOINT")
    TENCENT_STOCK_URL: str = Field(default="https://qt.gtimg.cn/q=", env="TENCENT_STOCK_URL")
    
    # 安全配置
    APP_SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="APP_SECRET_KEY")
    APP_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440, env="APP_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # 应用配置
    APP_DEBUG: bool = Field(default=True, env="APP_DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        if not self.DB_URL:
            self.DB_URL = (
                f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
                f"?charset=utf8mb4"
            )

settings = Settings()
