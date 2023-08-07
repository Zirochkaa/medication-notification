from beanie import Document, Indexed


class Medication(Document):
    name: Indexed(str)
    notification_time: str
    user_id: int

    class Settings:
        name = "medications"


class User(Document):
    username: Indexed(str, unique=True)
    user_id: int
    chat_id: int

    class Settings:
        name = "users"


# All models to instantiate on load
__beanie_models__ = [Medication, User]
