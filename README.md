# alexBot2.0
Guess I'm making the bot again

Open source version of alexBot code, not all the code is here because I'm too lazy to untangle it

## Setup
Run:
```
git clone https://github.com/justsomeonenamedalex/alexBot2.0
cd alexBot2.0
```
At this point I would advise you make a virtual enviroment. If you don't know how to, [follow this guide.](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)
With the virtualenv active, run the following command:
```
pip install -r requirements.txt
```

Next rename `config_example.json` to `config.json` and `discord.example.log` to `discord.log`. Then, make changes to config.json to use your api keys.

Then just run `bot.py` from the terminal with the following, or a similar, command:
```
python bot.py
```
