import asyncio

from googletrans import Translator

ENGLISH = "en"


def translate_text(text: str, destination: str = ENGLISH) -> str:
    translated = asyncio.run(Translator().translate(text, dest=destination))
    return translated.text
