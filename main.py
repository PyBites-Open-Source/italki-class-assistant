from db import store_translation, retrieve_translations
from translate import translate_text


def main():
    while True:
        destination = input("Enter target language (q to exit): ")
        if destination == "q":
            print("Exiting...")
            break

        while True:
            text = input("Enter text to translate (q to quit, p to print history): ")
            if text == "q":
                break

            if text == "p":
                print("Translation History:")
                translations = retrieve_translations(destination)
                for row in translations:
                    print(f"{row.text:<50} | {row.translated_text}")
                print()
                continue

            translated_text = translate_text(text, destination)
            print(translated_text)
            store_translation(text, destination, translated_text)


if __name__ == "__main__":
    main()
