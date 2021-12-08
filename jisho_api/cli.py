import json
import pprint
from pathlib import Path

import click
from rich.progress import Progress, track
from rich.prompt import Prompt

from jisho_api import console
from jisho_api.kanji.request import Kanji
from jisho_api.sentence.request import Sentence
from jisho_api.word.request import Word
from jisho_api.tokenize.request import Tokens


@click.group()
def main():
    """A jisho.org API. Test the API, or search the Japanese dictionary."""
    pass


@click.group()
def search():
    """Search jisho.org for words, kanjis, or sentences."""
    pass


@click.group()
def scrape():
    """Scrape requests, given a list of search terms."""
    pass


@click.command(name="config")
def config():
    """Set ~/.jisho/config.json with cache settings."""
    val = click.confirm("Cache enabled?")
    p = Path.home() / ".jisho"
    p.mkdir(exist_ok=True)
    with open(p / "config.json", "w") as fp:
        json.dump({"cache": val}, fp, indent=4)
    console.print("Config written to '.jisho/config.json'")


def _get_home_config():
    p = Path.home() / ".jisho/config.json"
    if p.exists():
        with open(p, "r") as fp:
            return json.load(fp)
    else:
        return None


def _cache_enabled():
    cfg = _get_home_config()
    if cfg:
        return cfg["cache"]
    return False


def scraper(cls, words, root_dump, cache=True):
    words = {}
    with Progress(console=console, transient=True) as progress:
        task1 = progress.add_task("[green]Scraping...", total=len(words))
        for i, w in enumerate(words):
            # 0 - name should be between quotes to search specifically for it
            # with a * it is a wildcard, to see applications of this word at the end
            strict = "*" not in w
            if strict:
                w = f'"{w}"'

            # 1 - if file exists do not request
            word_path = root_dump / f"{w}.json"
            if word_path.exists():
                progress.advance(task1)
                continue

            # 2 - make request
            wr = cls.request(w, cache=cache)
            if wr is None:
                progress.advance(task1)
                continue
            words[w] = wr

            progress.advance(task1)
    return words


def _load_words(file_path):
    with open(file_path, "r") as fp:
        txt = fp.read()
    words = txt.split("\n")
    return words


@click.command(name="word")
@click.argument("file_path")
def scrape_words(file_path: str):
    """Scrape list of words in txtfile, separated by newline."""
    root_dump = Word.ROOT
    root_dump.mkdir(parents=True, exist_ok=True)

    scraper(Word, _load_words(file_path), root_dump)


@click.command(name="kanji")
@click.argument("file_path")
def scrape_kanji(file_path: str):
    """Scrape list of kanji in txtfile, separated by newline."""
    root_dump = Kanji.ROOT
    root_dump.mkdir(parents=True, exist_ok=True)

    scraper(Kanji, _load_words(file_path), root_dump)


@click.command(name="sentence")
@click.argument("file_path")
def scrape_sentence(file_path: str):
    """Scrape list of sentence in txtfile, separated by newline."""
    root_dump = Sentence.ROOT
    root_dump.mkdir(parents=True, exist_ok=True)

    scraper(Sentence, _load_words(file_path), root_dump)

@click.command(name="tokens")
@click.argument("file_path")
def scrape_tokens(file_path: str):
    """Scrape list of tokens in txtfile, separated by newline."""
    root_dump = Tokens.ROOT
    root_dump.mkdir(parents=True, exist_ok=True)

    scraper(Tokens, _load_words(file_path), root_dump)


@click.command(name="word")
@click.argument("word")
@click.option("--cache", type=bool, is_flag=True)
@click.option("--no-cache", type=bool, is_flag=True)
def request_word(word: str, cache: bool, no_cache: bool):
    """Uses jisho.org word search API.
    """
    flag = (cache or _cache_enabled()) and not no_cache
    w = Word.request(word, cache=flag)
    if w:
        w.rich_print()


@click.command(name="kanji")
@click.argument("kanji")
@click.option("--cache", type=bool, is_flag=True)
@click.option("--no-cache", type=bool, is_flag=True)
def request_kanji(kanji: str, cache: bool, no_cache: bool):
    """Uses #kanji filter on jisho.org search engine.
    """
    flag = (cache or _cache_enabled()) and not no_cache
    k = Kanji.request(kanji, cache=flag)
    if k:
        k.rich_print()


@click.command(name="sentence")
@click.argument("sentence")
@click.option("--cache", type=bool, is_flag=True)
@click.option("--no-cache", type=bool, is_flag=True)
def request_sentence(sentence: str, cache: bool, no_cache: bool):
    """Uses #sentences filter on jisho.org search engine.
    """
    flag = (cache or _cache_enabled()) and not no_cache
    k = Sentence.request(sentence, cache=flag)
    if k:
        k.rich_print()

@click.command(name="tokens")
@click.argument("sentence")
@click.option("--cache", type=bool, is_flag=True)
@click.option("--no-cache", type=bool, is_flag=True)
def request_tokens(sentence: str, cache: bool, no_cache: bool):
    """jisho.org default search engine tokenizer.
    """
    flag = (cache or _cache_enabled()) and not no_cache
    k = Tokens.request(sentence, cache=flag)
    if k:
        k.rich_print()


# =============
# ==== CLI ====
# =============
def make_cli():
    scrape.add_command(scrape_words)
    scrape.add_command(scrape_kanji)
    scrape.add_command(scrape_sentence)

    search.add_command(request_word)
    search.add_command(request_kanji)
    search.add_command(request_sentence)
    search.add_command(request_tokens)

    main.add_command(scrape)
    main.add_command(search)
    main.add_command(config)
    main()


if __name__ == "__main__":
    make_cli()
