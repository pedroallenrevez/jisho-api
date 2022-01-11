from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, HttpUrl
from rich.markdown import Markdown

from jisho_api.cli import console
from jisho_api.util import CLITagger


class JLPT(str, Enum):
    N5 = "N5"
    N4 = "N4"
    N3 = "N3"
    N2 = "N2"
    N1 = "N1"


class MainReadings(BaseModel):
    kun: Optional[List[str]]
    on: Optional[List[str]]


class KanjiRadical(BaseModel):
    alt_forms: Optional[List[str]]
    meaning: str
    parts: List[str]
    basis: str
    kangxi_order: Optional[int]
    variants: Optional[List[str]]


class KanjiMeta(BaseModel):
    class KanjiMetaEducation(BaseModel):
        grade: Optional[str]
        jlpt: Optional[JLPT]
        newspaper_rank: Optional[int]

    class KanjiMetaReadings(BaseModel):
        japanese: Optional[List[str]]
        chinese: Optional[List[str]]
        korean: Optional[List[str]]

    education: Optional[KanjiMetaEducation]
    dictionary_idxs: Dict[str, str]
    classifications: Dict[str, str]
    codepoints: Dict[str, str]
    readings: KanjiMetaReadings


class ReadingExamples(BaseModel):
    class Example(BaseModel):
        kanji: str
        reading: str
        meanings: List[str]

    kun: Optional[List[Example]]
    on: Optional[List[Example]]


class KanjiConfig(BaseModel):
    kanji: str
    strokes: int
    main_meanings: List[str]
    main_readings: MainReadings
    meta: KanjiMeta
    radical: KanjiRadical
    # relation to words
    # on and kun are verifiable properties of the graph
    reading_examples: Optional[ReadingExamples]
