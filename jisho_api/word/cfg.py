from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Sense(BaseModel):
    class Link(BaseModel):
        text: str
        url: HttpUrl

    class Source(BaseModel):
        language: str

    english_definitions: List[str]
    parts_of_speech: List[Optional[str]]
    links: List[Link]
    tags: List[str]
    restrictions: List[str]
    see_also: List[str]
    antonyms: List[str]
    source: List[Source]
    info: List[str]


class Japanese(BaseModel):
    # Japanese Word - full fledged kanji
    # Is optional because there are words that are just kana
    word: Optional[str]
    # Kana reading
    reading: Optional[str]

    @property
    def name():
        if self.word:
            return self.word
        return self.reading


class WordConfig(BaseModel):
    slug: str
    is_common: Optional[bool]
    tags: List[str]

    jlpt: List[str]
    japanese: List[Japanese]
    senses: List[Sense]

    def __iter__(self):
        yield from self.senses
