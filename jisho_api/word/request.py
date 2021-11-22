import json
import pprint
import urllib
from pathlib import Path
from typing import List

import requests
from pydantic import BaseModel, ValidationError, validator
from rich.markdown import Markdown

from jisho_api import console

from .cfg import WordConfig


class RequestMeta(BaseModel):
    status: int


class WordRequest(BaseModel):
    meta: RequestMeta
    data: List[WordConfig]

    def __iter__(self):
        yield from reversed(self.data)

    def __len__(self):
        return len(self.data)

    def rich_print(self):
        for wdef in self:
            j = wdef.japanese[0]
            if j.word:
                base = f"[green]{j.word}"
                if j.reading is not None:
                    base += f" [red]([white]{j.reading}[red])"
            else:
                base = f"[green]{j.reading}"

            # TODO - really funky here
            if len(wdef.japanese) > 1:
                for j in wdef.japanese[1:]:
                    if j.word:
                        base += f", [purple]{j.word}"
                        if j.reading is not None:
                            base += f" [red]([white]{j.reading}[red])"
                    else:
                        base += f", [purple]{j.reading}"

            if len(wdef.jlpt):
                base += f" [blue][JLPT: {', '.join(wdef.jlpt)}]"
            console.print(base)

            for i, s in enumerate(wdef):
                base = f"[yellow]{i+1}. [white]{', '.join(s.english_definitions)}"
                base += "".join([f", ([magenta]{t}[white])" for t in s.tags])
                console.print(base)
            console.print(Markdown("---"))


class Word:
    URL = "https://jisho.org/api/v1/search/words?keyword="
    ROOT = Path.home() / ".jisho/data/word"

    @staticmethod
    def request(word, cache=False):
        url = Word.URL + urllib.parse.quote(word)
        toggle = False

        if cache and (Word.ROOT / (word + ".json")).exists():
            toggle = True
            with open(Word.ROOT / (word + ".json"), "r") as fp:
                r = json.load(fp)
        else:
            r = requests.get(url).json()
        r = WordRequest(**r)
        if not len(r):
            console.print(f"[red bold][Error] [white] No matches found for {word}.")
            return None

        if cache and not toggle:
            Word.save(word, r)
        return r

    @staticmethod
    def save(word, r):
        Word.ROOT.mkdir(exist_ok=True)
        with open(Word.ROOT / f"{word}.json", "w") as fp:
            fp.write(json.dumps(r.dict(), indent=4, ensure_ascii=False))
