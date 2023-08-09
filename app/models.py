from __future__ import annotations
from beanie import Document, Indexed


class Medication(Document):
    name: Indexed(str)
    notification_time: str
    user_id: int

    class Settings:
        name = "medications"

    @classmethod
    async def get_medications(cls, user_id: int) -> list[Medication]:
        return await Medication.find({"user_id": user_id}).sort("notification_time").to_list()


class User(Document):
    username: Indexed(str, unique=True)
    user_id: int
    chat_id: int

    class Settings:
        name = "users"


# All models to instantiate on load
__beanie_models__ = [Medication, User]
