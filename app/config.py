from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False

    app_base_url: str

    telegram_bot_token: str

    mongo_host: str = "127.0.0.1"
    mongo_port: int = 27017
    mongo_user: str = ""
    mongo_password: str = ""
    mongo_db_name: str = "medication_notification"

    model_config = SettingsConfigDict(env_file=".env")

    def mongodb_url(self) -> str:
        url = "mongodb://"

        if self.mongo_user and self.mongo_password:
            url += f"{self.mongo_user}:{self.mongo_password}@"

        url += f"{self.mongo_host}:{self.mongo_port}/{self.mongo_db_name}"
        return url

    def telegram_webhook_path(self) -> str:
        return f"/bot/{self.telegram_bot_token}"

    def telegram_webhook_url(self) -> str:
        return f"{self.app_base_url}{self.telegram_webhook_path()}"


settings = Settings()
