from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  frontend_origins: str
  postgres_user: str
  postgres_pass: str
  postgres_host: str
  postgres_port: str
  postgres_database_name: str
  jwt_secret_key: str
  jwt_algorithm: str
  hashing_secret_key: str
  access_token_expires: int
  refresh_token_expires: int
  google_client_id: str
  google_client_secret: str
  google_redirect_uri: str
  
  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
