import math

import FreeSimpleGUI as sg
import pyperclip
from decouple import config
from googletrans import LANGUAGES

from db import (
    clear_translations,
    due_cards,
    record_answer,
    retrieve_translations,
    store_translation,
)
from review import local_today
from translate import translate_text

SEPARATOR = "→"

# Set a custom theme with larger fonts
sg.set_options(font=("Any 16"))

DEFAULT_LANG_CODE = config("ITALKI_ACTIVATE_LANGUAGE_CODE", default="en")
DEFAULT_LANG_NAME = LANGUAGES[DEFAULT_LANG_CODE]

LAYOUT = [
    [
        sg.Combo(
            values=list(LANGUAGES.values()),
            default_value=DEFAULT_LANG_NAME,
            key="-LANGUAGE-",
            enable_events=True,
            readonly=True,
        ),
        sg.Button("Translate", bind_return_key=True),
    ],
    [sg.Input(key="-TEXT-", size=(50, 1))],
    [sg.Listbox(key="-OUT LIST-", size=(50, 10), values=[])],
    [
        sg.Button("Copy Selected Item", key="-COPY-"),
        sg.Button("Clear Saved", key="-CLEAR-"),
        sg.Button("Review", key="-REVIEW-"),
    ],
]

WINDOW = sg.Window("Italki Class Assistant", LAYOUT)


def update_output(lang_code):
    translations = retrieve_translations(lang_code)

    output_values = []
    for translation in translations:
        output_values.append(
            f"{translation.text} {SEPARATOR} {translation.translated_text}"
        )

    WINDOW["-OUT LIST-"].update(output_values)


def review(lang_code: str) -> None:
    cards = due_cards(lang_code, local_today())
    if not cards:
        sg.popup("Nothing due for review.", title="Review")
        return

    for card in cards:
        if sg.popup_ok(card.text, title="Review") is None:
            return
        answer = sg.popup_yes_no(
            f"{card.text} {SEPARATOR} {card.translated_text}\n\nKnew it?",
            title="Review",
        )
        if answer is None:
            return
        record_answer(card.id, answer == "Yes", local_today())


def main():
    WINDOW.finalize()
    update_output(DEFAULT_LANG_CODE)
    lang_code = DEFAULT_LANG_CODE

    while True:
        event, values = WINDOW.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-LANGUAGE-" or event == "Translate":
            lang_code = [
                code
                for code, name in LANGUAGES.items()
                if name == values["-LANGUAGE-"]
            ][0]

            if event == "Translate":
                text = values["-TEXT-"]
                translated = translate_text(text, lang_code)
                store_translation(text, lang_code, translated)

            # Load previous translations from the database
            update_output(lang_code)

        if event == "-COPY-":
            listbox: sg.Listbox = WINDOW["-OUT LIST-"]
            selected_idxs = listbox.GetIndexes()
            if len(selected_idxs) > 0:
                value: str = listbox.GetListValues()[selected_idxs[0]]
                sep_count = value.count(SEPARATOR)
                sep_idx = math.ceil(sep_count / 2)
                pyperclip.copy(value.split(SEPARATOR, sep_idx)[-1].strip())

        if event == "-CLEAR-":
            print(clear_translations(lang_code))
            update_output(lang_code)

        if event == "-REVIEW-":
            review(lang_code)

    WINDOW.close()


if __name__ == "__main__":
    main()
