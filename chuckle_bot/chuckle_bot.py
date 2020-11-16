from chuckle_bot.parser import parse_message
from chuckle_bot.parser import ParseError
from chuckle_bot.simple_logging import Logger
from chuckle_bot.single_channel_bot import Bot

from chuckle_bot import command
from chuckle_bot import roll

import discord


def make_chuckle_bot(guild_name, channel_id, players, characters, chuckles):
    """ Make the ChuckleBot

    :param guild_name: The name of the Discord Guild
    :type guild_name: string

    :param channel_id: The ID of the channel within the guild to monitor
    :type channel_id: int

    :param players: The players which are allowed to interact with the bot
    :type players: chuckle_bot.members.Members
    """

    logger = Logger()

    bot_intents = discord.Intents.default()
    bot_intents.members = True

    bot = Bot(guild_name, channel_id, logger, intents=bot_intents)

    command_handler = command.CommandHandler()

    async def help_handler(cmd):
        if (data := cmd.message.strip()) != "":
            response = command_handler.help_with(data)
        else:
            response = command_handler.help()
        await bot.send_message(response)

    async def begone_handler(cmd):
        if 'quiet' not in cmd.flags:
            await bot.send_message("Farewell")
        await bot.close()
        return

    async def hello_handler(cmd):
        char_id = players.get_char_id(cmd.sender)
        char_name = characters.get(char_id).name
        await bot.send_message("Hello " + char_name)

    async def roll_handler(cmd):
        adv = "advantage" in cmd.flags
        disadv = "disadvantage" in cmd.flags
        stats = characters.get(players.get_char_id(cmd.sender))
        await bot.send_message(roll.get_response(cmd.message, stats, adv, disadv))

    async def chuckles_handler(cmd):
        if "all" in cmd.flags:
            all_chuckles = chuckles.get_all()
            data_strs = []
            for char_id, count in all_chuckles:
                char_name = characters.get(char_id).full_name
                data_str = char_name + ": " + str(count)
                data_strs.append(data_str)
            msg = "\n".join(data_strs)
        else:
            char_id = players.get(cmd.sender)["CHAR_ID"]
            player_name = characters.get(char_id).full_name
            chuckles_caused = chuckles.get_count(char_id)
            msg = player_name + " has caused " + str(chuckles_caused) + " Chultian chuckles!"
        await bot.send_message(msg)

    command_handler.register_command(
        command.CommandType('begone', 'Disconnect the bot'),
        begone_handler,
        flags=[
            command.CommandOptionIdentifier(
                'quiet', 'q', 'Leaves without saying goodbye. Rude.')
        ]
    )
    command_handler.register_command(
        command.CommandType('chuckles', 'Get the current chuckle tally'),
        chuckles_handler,
        flags=[
            command.CommandOptionIdentifier('all', 'a', "Show everyone's chuckles")
        ]
    )
    command_handler.register_command(
        command.CommandType('hello', 'Say hello!'),
        hello_handler
    )
    command_handler.register_command(
        command.CommandType('help', 'Print this help message.'),
        help_handler
    )
    command_handler.register_command(
        command.CommandType('roll', 'Roll some dice...'),
        roll_handler,
        flags=[
            command.CommandOptionIdentifier('advantage', 'adv', 'Roll with advantage!'),
            command.CommandOptionIdentifier('disadvantage', 'disadv', 'Roll with disadvantage!'),
        ]
    )

    async def handle_message(message):
        try:
            cmd = parse_message(message)
            logger.log_message(cmd)
        except ParseError as exc:
            await bot.send_message("Sorry, I didn't get that")
        try:
            if cmd is not None:
                await command_handler.handle(cmd)
        except command.CommandException as exc:
            await bot.send_message(exc.msg)

    bot.set_ready_message("Chuckle!")
    bot.set_message_handler(handle_message)
    return bot
