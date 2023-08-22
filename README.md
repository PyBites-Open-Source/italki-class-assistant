# Italki Class Assistant

This script / repo is to quickly look up words in different target languages as I am talking with my teachers on Italki 💪

It uses [Googletrans](https://py-googletrans.readthedocs.io/en/latest/) but note that due to [an issue](https://github.com/ssut/py-googletrans/issues/383) it uses [a pre-release](https://pypi.org/project/googletrans/3.1.0a0/)

## Installation

1. Create Virtual Environment

    ```bash
    $ python3 -m venv venv
    ```

2. Activate Environment

    ```bash
    $ source venv/bin/activate # Mac/Linux
    $ venv\Scripts\activate # Windows
    ```

3. Install Dependencies

    ```bash
    $ pip install -r requirements.txt
    ```

4. Setup Database

    ```bash
    $ python3 db.py
    ```

5. (Optional) Copy `.env-template`

    ```bash
    $ cp .env-template .env
    ```
    `.env` file should now exist.

6. (Optional) Configure Default Language in `.env`

    If you want to start the app with a pre-selected language, you can set the `ITALKI_ACTIVATE_LANGUAGE_CODE` environment variable in the `.env` file.

    EXAMPLE:
    ```js
    ITALKI_ACTIVATE_LANGUAGE_CODE="fr"
    ```

## Running

1. Running GUI (Graphical User Interface)

    ```bash
    $ python3 gui.py
    ```

2. Running CLI (Cammand Line Interface)

    ```
    $ python3 main.py
    ```

Enjoy 😎 and boost your language learning 📈

<img width="661" alt="image" src="https://github.com/bbelderbos/italki-class-assistant/assets/387927/24515798-9f32-40b5-985e-9c424ed5fbe1">
