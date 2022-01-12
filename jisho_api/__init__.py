def scrape(cls, words, root_dump):
    from pathlib import Path
    cls.ROOT = Path(root_dump)
    nwords = {}
    for i, w in enumerate(words):
        # 0 - name should be between quotes to search specifically for it
        # with a * it is a wildcard, to see applications of this word at the end
        strict = "*" not in w
        if strict:
            w = f'"{w}"'

        # 1 - make request
        wr = cls.request(w, cache=True)
        if wr is None:
            continue
        nwords[w] = wr
    return nwords