class CLITagger:
    @staticmethod
    def colorize(tag, value, color, last=False):
        base = f"[{color}][{tag}: [white]{value}[{color}]]"
        if not last:
            base += " [white]| "
        return base

    @staticmethod
    def bullet(text, color="white"):
        return f"[yellow]• [{color}]{text}"


def flatten_recur(dct, rdct={}, separator=".", parent=""):
    for k, v in dct.items():
        if isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], dict):
                for i, l in enumerate(v):
                    flatten_recur(
                        l,
                        rdct,
                        parent=f"{parent}{k}{separator}{i}{separator}",
                        separator=separator,
                    )
            else:
                rdct[parent + k] = v
        elif not isinstance(v, dict):
            rdct[parent + k] = v
        else:
            flatten_recur(
                v, rdct, separator=separator, parent=f"{parent}{k}{separator}"
            )
    return rdct


def deflatten_recur(dct, rdct={}, separator="."):
    for k, v in dct.items():
        toks = k.split(separator)
        if len(toks) == 1:
            rdct[k] = v
        else:
            p = toks[0]
            toks = toks[1:]

            if toks[0].isdigit():
                idx = int(toks[0])
                # list
                if p not in rdct:
                    rdct[p] = []
                if len(rdct[p]) == idx:
                    rdct[p].append({})

                d = {separator.join(toks[1:]): v}
                deflatten_recur(d, rdct[p][idx], separator=separator)

            else:
                toks = separator.join(toks)

                if p not in rdct:
                    rdct[p] = {}
                d = {toks: v}

                deflatten_recur(d, rdct[p], separator=separator)
    return rdct
