from pydantic import BaseModel
from enum import Enum

class PosTag(Enum):
    noun="Noun"
    particle="Particle"
    verb="Verb"
    det="Determiner"
    conj="Conjunction"
    pron="Pronoun"
    unk='Unknown'

    # unexpected posTags get assigned the unknown enum.
    # implementation source: https://stackoverflow.com/questions/44867597/is-there-a-way-to-specify-a-default-value-for-python-enums
    @classmethod
    def _missing_(PosTag, value):
        return PosTag.unk

class TokenConfig(BaseModel):
    token: str
    pos_tag: PosTag
    #pos_tag: str
