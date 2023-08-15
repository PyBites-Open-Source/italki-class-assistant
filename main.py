import PySimpleGUI as sg
from translate import translate_text, LANGUAGES
from cache import get_translations_for_language


def create_window():
    sg.theme("LightGreen")

    layout = [
        [
            sg.Text("Choose a language to translate to:", font=("Helvetica", 20)),
            sg.Combo(
                list(LANGUAGES.values()),
                key="-LANG-",
                size=(20, 1),
                font=("Helvetica", 20),
            ),
        ],
        [
            sg.Text("Enter text to translate:", font=("Helvetica", 20)),
            sg.InputText(key="-TEXT-", size=(50, 5), font=("Helvetica", 20)),
        ],
        [
            sg.Button("Translate", bind_return_key=True, font=("Helvetica", 20)),
            sg.Button("Exit", font=("Helvetica", 20)),
        ],
        [
            sg.Text("Translation output:", size=(40, 1), font=("Helvetica", 20)),
        ],
        [sg.Listbox(values=[], size=(60, 10), key="-OUTPUT-", font=("Helvetica", 20))],
    ]

    return sg.Window(
        "Text Translator", layout, font=("Helvetica", 20), return_keyboard_events=True
    )


def main():
    window = create_window()
    translations = []
    prev_lang = None

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        target_language_key = {v: k for k, v in LANGUAGES.items()}[values["-LANG-"]]
        if target_language_key != prev_lang:
            prev_lang = target_language_key
            cached_entries = get_translations_for_language(target_language_key)
            translations = [
                f"{entry.source_text} - {entry.translated_text}"
                for entry in cached_entries
            ]
            window["-OUTPUT-"].update(translations)

        if event == "Translate":
            translated_text = translate_text(
                values["-TEXT-"], target=target_language_key
            )

            # Create a new entry for the translation
            translation_entry = f"{values['-TEXT-']} - {translated_text}"

            # Insert the new entry at the beginning of the translations list
            translations.insert(0, translation_entry)

            # Update the Listbox element to display the updated translations list
            window["-OUTPUT-"].update(translations)

    window.close()


if __name__ == "__main__":
    main()
