from chuckle_bot.simple_logging import Logger
from chuckle_bot.single_channel_bot import Bot

from chuckle_bot import roll

import discord


def make_chuckle_bot(guild_name, channel_id):
    """ Make the ChuckleBot

    :param guild_name: The name of the Discord Guild
    :type guild_name: string

    :param channel_id: The ID of the channel within the guild to monitor
    :type channel_id: int
    """

    COMMANDS = ['begone', 'roll']

    async def handle_message(message):
        content = message.content.lower()
        if content == '.begone':
            await bot.send_message("Farewell")
            await bot.close()
            return
        elif content.startswith('.roll ') or content.startswith('.r '):
            await bot.send_message(roll.get_response(content.split(' ', 1)[1]))
        else:
            msg = "I heard you..."
            await bot.send_message(msg)

    logger = Logger()
    bot = Bot(guild_name, channel_id, logger)

    bot.set_ready_message("Chuckle!")
    bot.set_message_handler(handle_message)
    return bot
