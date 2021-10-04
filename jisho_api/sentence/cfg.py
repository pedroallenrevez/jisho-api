from pydantic import BaseModel


class SentenceConfig(BaseModel):
    japanese: str
    en_translation: str
