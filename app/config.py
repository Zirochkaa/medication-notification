from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False

    app_base_url: str

    telegram_bot_token: str
    telegram_channel_id: Optional[int] = None

    database_url: str = "mongodb://127.0.0.1:27017/medication_notification"
    mongo_db_name: str = "medication_notification"
    mongo_db_name_test: str = "medication_notification_test"

    history_days_amount: int = 7

    model_config = SettingsConfigDict(env_file=".env")

    def telegram_webhook_path(self) -> str:
        return f"/bot/{self.telegram_bot_token}"

    def telegram_webhook_url(self) -> str:
        return f"{self.app_base_url}{self.telegram_webhook_path()}"


settings = Settings(_env_file="app/.env")
