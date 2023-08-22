import math

import pyperclip
import PySimpleGUI as sg
from decouple import config
from googletrans import LANGUAGES

from db import retrieve_translations, store_translation
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
    [sg.Button("Copy Selected Item", key="-COPY-")],
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


def main():
    WINDOW.finalize()
    update_output(DEFAULT_LANG_CODE)

    while True:
        event, values = WINDOW.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-LANGUAGE-" or event == "Translate":
            lang_code = [
                code for code, name in LANGUAGES.items() if name == values["-LANGUAGE-"]
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

    WINDOW.close()


if __name__ == "__main__":
    main()
