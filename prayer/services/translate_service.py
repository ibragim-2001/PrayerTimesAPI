from translate import Translator


def translate(word: str) -> str:
    ts = Translator(to_lang="ru")

    return ts.translate(word)