from pydantic import BaseModel
from enum import Enum

class PosTag(Enum):
    noun="Noun"
    particle="Particle"
    verb="Verb"
    det="Determiner"
    unk='Unknown'

class TokenConfig(BaseModel):
    token: str
    pos_tag: PosTag
    #pos_tag: str
