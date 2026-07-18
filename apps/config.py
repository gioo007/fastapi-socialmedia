from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str = "db hostname"
    database_port: str = "db port number"
    postgres_password: str = "db password"
    postgres_db: str = "db name"
    postgres_user: str = "db username"
    secret_key: str = "secret key"
    algorithm: str = "algorithm"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file= ".env")

settings = Settings()