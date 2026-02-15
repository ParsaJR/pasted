from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# class LogLevels(Enum):
#     Info = "info"
#     Debug = "debug"

# Envs.
# 1. Can be override at runtime. (Prefix Using "PASTED_")
# 2. Can be set also by the .env file in the project's root folder. ONLY IN DEVELOPMENT!
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='PASTED_',
        env_file=".env",
        env_file_encoding="utf-8"
    )

    ## General
    app_name: str = "Generic Pasted Service"
    contact_email: str = "hi@example.org"

    ## Database related
    DatabaseHost: str = "localhost"
    DatabasePort: int = 5432 # Postgres uses 5432 by default, for active listen port.
    DatabasePassword: str = "mysecretpassword"
    DatabaseUser: str = "postgres"
    DatabaseName: str = "pasted" 

    ## JWT Issues
    JWT_Secret: str
    JWT_TTL: int = 604_800



    


settings = Settings()   # pyright: ignore[reportCallIssue]
