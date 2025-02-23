from translate import Translator


def translate(word):
    ts = Translator(to_lang="ru")

    return ts.translate(word)