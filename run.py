from chuckle_bot import ally
from chuckle_bot import chuckle_bot
from chuckle_bot import chuckle_count
from chuckle_bot import members
from chuckle_bot import players

import json
import random

CONFIG_PATH = 'data/config.json'
CHARACTER_PATH = 'data/characters.json'
MEMBER_PATH = 'data/members.json'
CHUCKLECOUNT_PATH = 'data/chuckle_tally.json'
DEFAULT_ENCOUNTER_PATH = 'data/default_encounter.json'
ALLIES_PATH = 'data/allies.json'


def main():
    random.seed()

    with open(CONFIG_PATH) as fp:
        config = json.load(fp)

    with open(MEMBER_PATH) as fp:
        guild_members = members.Members(json.load(fp))

    with open(CHARACTER_PATH) as fp:
        dnd_characters = players.build_players(json.load(fp))

    with open(CHUCKLECOUNT_PATH) as fp:
        chuckles = chuckle_count.ChuckleCount(json.load(fp))

    with open(DEFAULT_ENCOUNTER_PATH) as fp:
        default_encounter_chars = dnd_characters.subset(json.load(fp)["CHARACTERS"])

    with open(ALLIES_PATH) as fp:
        possible_allies = ally.build_allies(json.load(fp))

    bot = chuckle_bot.make_chuckle_bot(config['GUILD_NAME'], config['CHANNEL_ID'],
                                       guild_members, dnd_characters, chuckles,
                                       default_encounter_chars,
                                       possible_allies)
    bot.run(config['BOT_TOKEN'])


if __name__ == '__main__':
    main()
