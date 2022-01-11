from enum import Enum

from pydantic import BaseModel


class PosTag(Enum):
    adj="Adjective"
    adv="Adverb"
    conj="Conjunction"
    det="Determiner"
    interjection="Interjection"
    noun="Noun"
    particle="Particle"
    pr_noun="Proper noun"
    prfx="Prefix"
    pron="Pronoun"
    sfx="Suffix"
    unk="Unknown"
    verb="Verb"

    # rather than causing the program to crash, inform the user of the unexpected posTag
    # implementation source: https://stackoverflow.com/questions/44867597/is-there-a-way-to-specify-a-default-value-for-python-enums
    @classmethod
    def _missing_(self, value):
        print("Unexpected positional Tag: {}".format(value))
        return self.unk

class TokenConfig(BaseModel):
    token: str
    pos_tag: PosTag
    #pos_tag: str
