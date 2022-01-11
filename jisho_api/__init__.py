def scrape(cls, words, root_dump, cache=True):
    from pathlib import Path
    root_dump = Path(root_dump)
    nwords = {}
    for i, w in enumerate(words):
        # 0 - name should be between quotes to search specifically for it
        # with a * it is a wildcard, to see applications of this word at the end
        strict = "*" not in w
        if strict:
            w = f'"{w}"'

        # 1 - if file exists do not request
        word_path = root_dump / f"{w}.json"
        if word_path.exists():
            continue

        # 2 - make request
        wr = cls.request(w, cache=cache)
        if wr is None:
            continue
        nwords[w] = wr
    return nwords