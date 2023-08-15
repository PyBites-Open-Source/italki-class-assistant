from googletrans import Translator


def main():
    print(translate_text("hello world", target="fr"))


def translate_text(text, target='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target)
    return translation.text


if __name__ == '__main__':
    main()

