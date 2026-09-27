# Italki Class Assistant

This script / repo is to quickly look up words in different target languages as I am talking with my teachers on Italki 💪

It uses [Googletrans](https://py-googletrans.readthedocs.io/en/latest/) for translations and [FreeSimpleGUI](https://github.com/spyoungtech/FreeSimpleGUI) for the GUI.

## Installation

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Install Dependencies

    ```bash
    $ uv sync
    ```

3. Setup Database

    ```bash
    $ uv run db.py
    ```

4. (Optional) Copy `.env-template`

    ```bash
    $ cp .env-template .env
    ```
    `.env` file should now exist.

5. (Optional) Configure Default Language in `.env`

    If you want to start the app with a pre-selected language, you can set the `ITALKI_ACTIVATE_LANGUAGE_CODE` environment variable in the `.env` file.

    EXAMPLE:
    ```js
    ITALKI_ACTIVATE_LANGUAGE_CODE="fr"
    ```

## Running

1. Running GUI (Graphical User Interface)

    ```bash
    $ uv run gui.py
    ```

2. Running CLI (Command Line Interface)

    ```
    $ uv run main.py
    ```

## Reviewing

Every word you look up becomes a flashcard. Review due cards with the **Review** button in the GUI or `r` in the CLI. Cards you know move up a box (review again in 1, 2, 4, 8, then 16 days); cards you miss go back to box 1. Looking a word up again during class also sends it back to box 1.

Run the tests with `uv run pytest`.

Enjoy 😎 and boost your language learning 📈

<img width="661" alt="image" src="https://github.com/bbelderbos/italki-class-assistant/assets/387927/24515798-9f32-40b5-985e-9c424ed5fbe1">
