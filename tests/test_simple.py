def test_imports():
    from jisho_api.word import Word
    from jisho_api.kanji import Kanji
    from jisho_api.sentence import Sentence

def test_word_request():
    from jisho_api.word import Word
    r = Word.request('water')

def test_kanji_request():
    from jisho_api.kanji import Kanji
    r = Kanji.request('水')

def test_sentence_request():
    from jisho_api.sentence import Sentence
    r = Sentence.request('water')
