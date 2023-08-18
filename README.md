# Italki Class Assistant

This script / repo is to quickly look up words in different target languages as I am talking with my teachers on Italki 💪

It uses [Googletrans](https://py-googletrans.readthedocs.io/en/latest/) but note that due to [an issue](https://github.com/ssut/py-googletrans/issues/383) it uses [a pre-release](https://pypi.org/project/googletrans/3.1.0a0/)

To use it make a virtual environment (Unix: `python -m venv venv && source venv/bin/activate`) and install the requirements (`pip install requirements.txt`), then:

```
python gui.py
```

If you want to start the app with a pre-selected language, you can set the `ITALKI_ACTIVATE_LANGUAGE_CODE` environment variable either in an `.env` file (locally in the project root folder) or from the command line, for example: `export ITALKI_ACTIVATE_LANGUAGE_CODE=fr`.

Enjoy 😎 and boost your language learning 📈

<img width="661" alt="image" src="https://github.com/bbelderbos/italki-class-assistant/assets/387927/24515798-9f32-40b5-985e-9c424ed5fbe1">

