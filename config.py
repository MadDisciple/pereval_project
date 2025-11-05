from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    FSTR_DB_HOST: str
    FSTR_DB_PORT: int
    FSTR_DB_LOGIN: str
    FSTR_DB_PASS: str
    FSTR_DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.FSTR_DB_LOGIN}:{self.FSTR_DB_PASS}@{self.FSTR_DB_HOST}:{self.FSTR_DB_PORT}/{self.FSTR_DB_NAME}"

settings = Settings()