from chuckle_bot.simple_logging import Logger
from chuckle_bot.single_channel_bot import Bot

from chuckle_bot import command
from chuckle_bot import roll

import discord


def make_chuckle_bot(guild_name, channel_id, players):
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
        sender = players.get(cmd.sender)
        await bot.send_message("Hello " + sender["CHAR_FULL"])

    async def roll_handler(cmd):
        await bot.send_message(roll.get_response(cmd.message))

    command_handler.register_command(
        command.CommandType('begone', 'Disconnect the bot'),
        begone_handler,
        flags=[
            command.CommandOptionIdentifier(
                'quiet', 'q', 'Leaves without saying goodbye. Rude.'
            )
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
        roll_handler
    )

    class ParseError(Exception):
        def __init__(self, msg=None):
            super().__init__()
            self.msg = msg

    def parse_message(message):
        """ Parse the message as a CommandInstance

        Return None if there is no command in the message
        Raise ParseError if the Command is not understood
        """

        if not message.content.startswith('.'):
            return None
        if len(message.content) == 1:
            return None

        instruction_and_data = message.content[1:]
        if " " in instruction_and_data:
            instruction, data = instruction_and_data.split(' ', 1)
        else:
            instruction = instruction_and_data
            data = ""

        found_options = {}
        found_flags = []
        if '--' in data:
            data, flags = data.split('--', 1)
            flags = flags.replace('--', '')
            flags = flags.split(' ')
            flags = [flag.strip() for flag in flags]
            found_flags = [x for x in flags if len(x) != 0]

        if "=" in data and "-" in data:
            # Split at the first '-' before the data..
            lhs, rhs = data.split('=', 1)
            data, lhs = lhs.rsplit('-', 1)
            options = lhs + '=' + rhs
            options = options.replace('-', '')
            option_pairs = options.split(' ')
            option_pairs = [x.strip() for x in option_pairs]
            option_pairs = [x for x in option_pairs if len(x) != 0]
            for pair in option_pairs:
                key, val = pair.split('=')
                found_options[key] = val

        return command.CommandInstance(instruction, data, message.author.id,
                                       found_options, found_flags)

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
