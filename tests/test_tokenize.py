def test_tokens_tatoeba():
    import random

    from tatoebatools import tatoeba

    from jisho_api.tokenize import Tokens

    # there's multiple thousands of sentences in tatoeba so we'll only use 100 in order not to fry jisho, which would be very rude indeed
    japanese_texts = [s.text for s in tatoeba.sentences_detailed("jpn")]
    sentences = random.sample(japanese_texts, 5)
    
    for sentence in sentences:
        result = Tokens.request(sentence)

if __name__ == "__main__":
    test_tokens_tatoeba()
