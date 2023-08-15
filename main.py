import PySimpleGUI as sg
from translate import translate_text, LANGUAGES


def create_window():
    sg.theme("LightGreen")

    layout = [
        [
            sg.Text("Choose a language to translate to:"),
            sg.Combo(list(LANGUAGES.values()), key="-LANG-", size=(20, 1)),
        ],
        [
            sg.Text("Enter text to translate:"),
            sg.InputText(key="-TEXT-", size=(50, 5)),
        ],
        [sg.Button("Translate", bind_return_key=True), sg.Button("Exit")],
        [sg.Text("Translation output:", size=(40, 1))],
        [sg.Listbox(values=[], size=(60, 10), key="-OUTPUT-", font=("Helvetica", 12))],
    ]

    return sg.Window(
        "Text Translator", layout, font=("Helvetica", 14), return_keyboard_events=True
    )


def main():
    window = create_window()

    # List to store translations in the format "original - translated"
    translations = []

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        if event == "Translate":
            target_language_key = {v: k for k, v in LANGUAGES.items()}[values["-LANG-"]]
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
