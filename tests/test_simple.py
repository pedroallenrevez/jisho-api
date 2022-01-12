def test_imports():
    from jisho_api.kanji import Kanji
    from jisho_api.sentence import Sentence
    from jisho_api.tokenize import Tokens
    from jisho_api.word import Word

def test_word_request():
    from jisho_api.word import Word
    r = Word.request('water')
    assert r

def test_kanji_request():
    from jisho_api.kanji import Kanji
    r = Kanji.request('水')
    assert r

def test_sentence_request():
    from jisho_api.sentence import Sentence
    r = Sentence.request('water')
    assert r

def test_tokens_request():
    from jisho_api.tokenize import Tokens
    r = Tokens.request('昨日すき焼きを食べました')
    assert r

def test_scrape():
    from jisho_api import scrape
    from jisho_api.word import Word

    word_requests = scrape(Word, ['water', 'fire'], 'test')
    assert len(word_requests)