from googletrans import Translator

ENGLISH = "en"


def translate_text(text: str, destination: str = ENGLISH) -> str:
    translator = Translator()
    translated = translator.translate(text, dest=destination)
    return translated.text
