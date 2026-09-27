from db import (
    due_cards,
    record_answer,
    retrieve_translations,
    store_translation,
)
from review import local_today
from translate import translate_text


def review(destination: str) -> None:
    cards = due_cards(destination, local_today())
    if not cards:
        print("Nothing due for review.\n")
        return

    for card in cards:
        input(f"{card.text}  (enter to reveal) ")
        answer = input(f"{card.translated_text}  knew it? [y/n]: ")
        record_answer(card.id, answer.strip().lower() == "y", local_today())
    print(f"Reviewed {len(cards)} cards.\n")


def main():
    while True:
        destination = input("Enter target language (q to exit): ")
        if destination == "q":
            print("Exiting...")
            break

        while True:
            text = input(
                "Enter text to translate "
                "(q to quit, p to print history, r to review): "
            )
            if text == "q":
                break

            if text == "p":
                print("Translation History:")
                translations = retrieve_translations(destination)
                for row in translations:
                    print(f"{row.text:<50} | {row.translated_text}")
                print()
                continue

            if text == "r":
                review(destination)
                continue

            translated_text = translate_text(text, destination)
            print(translated_text)
            count = store_translation(text, destination, translated_text)
            if count > 1:
                print(f"(looked up {count}x, back in review)")


if __name__ == "__main__":
    main()
