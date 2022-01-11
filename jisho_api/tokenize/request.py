import json
import pprint
import re
import urllib
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
from rich.markdown import Markdown

from jisho_api.cli import console
from jisho_api.util import CLITagger

from .cfg import TokenConfig


class RequestMeta(BaseModel):
    status: int


class TokenRequest(BaseModel):
    meta: RequestMeta
    data: List[TokenConfig]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        yield from self.data

    def rich_print(self):
        base = ''
        toks = ''
        for i, d in enumerate(self):
            base += CLITagger.underline(d.token) + ' '
            toks += f"{i}. {d.token} [violet][{str(d.pos_tag.value)}][/violet]\n"
        console.print(base)
        console.print(toks)


class Tokens:
    URL = "https://jisho.org/search/"
    ROOT = Path.home() / ".jisho/data/tokens/"

    @staticmethod
    def tokens(soup):
        res = soup.find_all("section", {"id": "zen_bar"})

        tks = []
        for r in res:
            toks = r.find_all("li")
            for t in toks:
                try:
                    pos_tag = t['data-pos']
                except:
                    pos_tag = "Unknown"
                jp = t.find_all('span', {"class": "japanese_word__text_wrapper"})
                try:
                    jp = jp[0].find_all('a')[0]['data-word']
                except Exception as e:
                    jp = jp[0].text.strip()
                tks.append(TokenConfig(
                    token=jp,
                    pos_tag=pos_tag
                ))

        return tks

    @staticmethod
    def request(word, cache=False):
        url = Tokens.URL + urllib.parse.quote(word)
        toggle = False

        if cache and (Tokens.ROOT / (word + ".json")).exists():
            toggle = True
            with open(Tokens.ROOT / (word + ".json"), "r") as fp:
                r = json.load(fp)
            r = TokenRequest(**r)
        else:
            r = requests.get(url).content
            soup = BeautifulSoup(r, "html.parser")

            r = TokenRequest(
                **{
                    "meta": {
                        "status": 200,
                    },
                    "data": Tokens.tokens(soup),
                }
            )
            if not len(r):
                console.print(f"[red bold][Error] [white] No matches found for {word}.")
                return None
        if cache and not toggle:
            Tokens.save(word, r)
        return r

    @staticmethod
    def save(word, r):
        Tokens.ROOT.mkdir(exist_ok=True)
        with open(Tokens.ROOT / f"{word}.json", "w") as fp:
            json.dump(r.dict(), fp, indent=4, ensure_ascii=False)
