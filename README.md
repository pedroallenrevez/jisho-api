# jisho-api

A Python API built around scraping https://jisho.org, an online Japanese dictionary.

## Requests

You can request three types of information:
- Words
- Kanji
- Sentences

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
from jisho.word import Word
r = Word.request('water')
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
```
All of the resulting searches will be stored in `~/.jisho/data`.

In case you want to scrape programatically you can:
```python
from jisho.cli import scrape
from jisho.word import Word

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