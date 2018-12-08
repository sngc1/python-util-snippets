import MeCab


def kanji2kana(kanji: str) -> str:
    tagger = MeCab.Tagger ("-Ochasen")
    parsed = tagger.parse(kanji)
    kana = []
    for line in parsed.split("\n"):
        parsed = line.split("\t")
        if len(parsed) > 1:
            kana.append(parsed[1])
    return ' '.join(kana)

if __name__ == '__main__':
    print(kanji2kana('本日は気持ちよく晴れるでしょう'))