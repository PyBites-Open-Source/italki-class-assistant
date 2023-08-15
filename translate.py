from googletrans import Translator, LANGUAGES

from cache import cache_translation


def main():
    while True:
        target = input("Choose a language to translate to (type 'q' to exit): ")
        if target == "q":
            break
        if target not in LANGUAGES:
            print(f'Invalid target language, valid are: {", ".join(LANGUAGES)}')
            continue

        while True:
            text = input(
                f"Enter text to translate to {LANGUAGES[target]} (type 'q' to change language): "
            )
            if text == "q":
                break
            translated = translate_text(text, target=target)
            print(translated)


@cache_translation
def translate_text(text: str, target: str = "en") -> str:
    translator = Translator()
    translation = translator.translate(text, dest=target)
    return translation.text


if __name__ == "__main__":
    main()
