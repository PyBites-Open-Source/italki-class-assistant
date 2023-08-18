from datetime import datetime

import PySimpleGUI as sg
from googletrans import LANGUAGES, Translator

from db import store_translation, retrieve_translations
from models import Translation
from translate import translate_text

# Set a custom theme with larger fonts
sg.set_options(font=("Any 16"))

layout = [
    [
        sg.Combo(
            values=list(LANGUAGES.values()),
            default_value="English",
            key="-LANGUAGE-",
            enable_events=True,
            readonly=True,
        ),
        sg.Button("Translate", bind_return_key=True),
    ],
    [sg.Input(key="-TEXT-", size=(50, 1))],
    [sg.Multiline(key="-OUTPUT-", size=(50, 10), disabled=True, autoscroll=True)],
]

window = sg.Window("Translator", layout)

while True:
    event, values = window.read()

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
        translations = retrieve_translations(lang_code)

        output = ""
        for translation in translations:
            output += f"{translation.text} -> {translation.translated_text}\n"

        window["-OUTPUT-"].update(output)


window.close()
