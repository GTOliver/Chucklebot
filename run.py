from chuckle_bot import chuckle_bot

import json


def main():
    with open("config.json") as fp:
        config = json.load(fp)

    bot = chuckle_bot.make_chuckle_bot(config['GUILD_NAME'], config['CHANNEL_ID'])
    bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
    main()
