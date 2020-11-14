from chuckle_bot import chuckle_bot
from chuckle_bot import members

import json

CONFIG_PATH = 'data/config.json'
MEMBER_PATH = 'data/members.json'


def main():
    with open(CONFIG_PATH) as fp:
        config = json.load(fp)

    with open(MEMBER_PATH) as fp:
        guild_members = members.Members(json.load(fp))

    bot = chuckle_bot.make_chuckle_bot(config['GUILD_NAME'], config['CHANNEL_ID'], guild_members)
    bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
    main()
