from chuckle_bot import chuckle_bot
from chuckle_bot import chuckle_count
from chuckle_bot import members
from chuckle_bot import characters

import json

CONFIG_PATH = 'data/config.json'
CHARACTER_PATH = 'data/characters.json'
MEMBER_PATH = 'data/members.json'
CHUCKLECOUNT_PATH = 'data/chuckle_tally.json'


def main():
    with open(CONFIG_PATH) as fp:
        config = json.load(fp)

    with open(MEMBER_PATH) as fp:
        guild_members = members.Members(json.load(fp))

    with open(CHARACTER_PATH) as fp:
        dnd_characters = characters.Characters(json.load(fp))

    with open(CHUCKLECOUNT_PATH) as fp:
        chuckles = chuckle_count.ChuckleCount(json.load(fp))

    bot = chuckle_bot.make_chuckle_bot(config['GUILD_NAME'], config['CHANNEL_ID'],
                                       guild_members, dnd_characters, chuckles)
    bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
    main()
