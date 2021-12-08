# jisho-api

[![GitHub tag](https://img.shields.io/github/tag/pedroallenrevez/jisho-api)](https://github.com/pedroallenrevez/jisho-api/releases/?include_prereleases&sort=semver "View GitHub releases")

A Python API built around scraping [jisho.org](https://jisho.org), an online Japanese dictionary.

```bash
pip install jisho_api
```

[![asciicast](https://asciinema.org/a/NJuZQnNfe0JDdDELn08NhmYuY.svg)](https://asciinema.org/a/NJuZQnNfe0JDdDELn08NhmYuY)

## Requests
You can request three types of information:
- Words
- Kanji
- Sentences
- Tokenize sentences

The search terms are directly injected into jisho's search engine, which means all of 
the filters used to curate a search should work as well. For instance, `"水"` would look 
precisely for a word with just that character.

Check https://jisho.org/docs on how to use the search filters.

```bash
jisho search word water
jisho search word 水
jisho search word "#jlpt-n4"
```

The request replies are [Pydantic](https://pydantic-docs.helpmanual.io/) objects.
You can check the structure of a word request in `jisho/word/cfg.py`, and likewise for both kanji and sentences.

You could also do so programatically, by doing:
```python
from jisho_api.word import Word
r = Word.request('water')
from jisho_api.kanji import Kanji
r = Kanji.request('水')
from jisho_api.sentence import Sentence
r = Sentence.request('水')
from jisho_api.tokenize import Tokens
r = Tokens.request('昨日すき焼きを食べました')
```

> **Note**: Almost everything that is available in a page is being scraped.
> **Note**: Kanji requests can come with incomplete information, because it is not available in the page.

## Scrapers
You can scrape the website for a list of given search terms.
Supply them with a `.txt` file with the words separated by newlines.

```bash
jisho scrape word words.txt
jisho scrape kanji kanji.txt
jisho scrape sentence search_words.txt
jisho scrape tokens sentences.txt
```
All of the resulting searches will be stored in `~/.jisho/data`.

In case you want to scrape programatically you can:
```python
from jisho_api.cli import scrape
from jisho_api.word import Word

word_requests = scrape(Word, ['water', 'fire'], '/to/path')
```
This will return a dictionary, which key values are the search term and request result.
Failing requests are not included.

## Cache and config
If you want cache enabled just run 
```bash
jisho config
```

This will create a `~/.jisho/` folder with a `config.json` with your settings.
All your searches will be cached, and accessed if you search for the exact same term again.

## Notes and considerations
According to this [thread](https://jisho.org/forum/54fefc1f6e73340b1f160000-is-there-any-kind-of-search-api),
there is no official API, although there is a kind of [API request](https://jisho.org/api/v1/search/words?keyword=house) made by jisho.org, which is used to scrape words. This does not work for Kanji tho,
because it would search the Kanji as a word, and not have any relevant metadata for the character itself.

Permissions to scrape also granted in the aforementioned thread.

As stated in their [about page](https://jisho.org/docs) as well, jisho.org uses a collection of well-known [electronic dictionaries](http://www.edrdg.org/):
> This site uses the JMdict, Kanjidic2, JMnedict and Radkfile dictionary files. -jisho.org

## Credits and Acknowledgements for data
All credit is given where it's due, and the several extracted resources is given at jisho.org's [about page](https://jisho.org/docs).
