### [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)  [![Aiogram](https://img.shields.io/badge/aiogram-2.12-blue)](https://pypi.org/project/aiogram/) 

### About
Scalable and straightforward template for bots written on [aiogram](https://github.com/aiogram/aiogram).

### Setting up

#### System dependencies
- Python 3.9+
- GNU/Make 
- GIT

#### Preparations
- Clone this repo via `git clone https://github.com/f0rzend/aiogram_template`;
- Move to the directory `cd aiogram_template`.

#### Poetry Deployment
- **Note:** You need to have Poetry installed: `pip install poetry`;
- Install dependencies: `make install`;
- Rename `config.yml.tmp` to `config.yml` and replace a token placeholder with your own one;
- Start the bot: `make run`.

**Tip**: set `BOT_CONFIG_FILE` environment variable to change config path. If no variable is specified, it'll assume it's located in `bot/config/config.yml`.


#### Maintenance
*Use `make help` to view available commands*

- Update dependencies `make update`;
- Reformat code `make lint`.
