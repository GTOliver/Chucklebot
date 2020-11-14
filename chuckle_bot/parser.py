from chuckle_bot import command


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
