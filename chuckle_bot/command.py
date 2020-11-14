class CommandException(Exception):
    def __init__(self, msg=''):
        self.msg = msg


class CommandType:
    def __init__(self, trigger, description):
        self.trigger = trigger
        self.description = description
        self._options = []
        self._flags = []


class CommandInstance:
    def __init__(self, name, message, sender, options=[], flags=[]):
        self.name = name
        self.message = message
        self.sender = sender
        self.options = options
        self.flags = flags

    def __repr__(self):
        return " ".join([str(s) for s in [
            "Command:", self.name, self.message, self.sender, self.options, self.flags]])


class CommandOptionIdentifier:
    def __init__(self, full, abbreviation, description):
        self.full = full
        self.abrv = abbreviation
        self.desc = description

    def __eq__(self, other_string):
        return other_string == self.full or other_string == self.abrv


class CommandHandler:
    def __init__(self):
        self._commands = []
        self._handlers = []
        self._options = []
        self._flags = []

    def _get_idx_of(self, name):
        for i in range(len(self._commands)):
            if self._commands[i].trigger == name:
                return i
        return None

    async def handle(self, command):
        idx = self._get_idx_of(command.name)
        if idx is None:
            raise CommandException("Sorry, I don't know what '" + command.name + "' means")
        # Convert options_or_flags to use full versions
        new_options = {}
        for option_key in command.options:
            option_found = False
            for known_option in self._options[idx]:
                if option_key == known_option:
                    new_options[known_option.full] == command.options[option_key]
                    option_found = True
                    break
            if not option_found:
                raise CommandException("Option " + option_key + " not recognised")
        new_flags = []
        for flag in command.flags:
            flag_found = False
            for known_flag in self._flags[idx]:
                if flag == known_flag:
                    new_flags.append(known_flag.full)
                    flag_found = True
                    break
            if not flag_found:
                raise CommandException("Flag " + flag + " not recognised")

        new_command = CommandInstance(command.name, command.message, command.sender,
                                      new_options, new_flags)
        return await self._handlers[idx](new_command)

    def register_command(self, command, handler, options=[], flags=[]):
        self._commands.append(command)
        self._handlers.append(handler)
        self._options.append(options)
        self._flags.append(flags)

    def help(self):
        msg = "Available commands:\n"
        msg += '---\n'
        for cmd in self._commands:
            msg += "    ." + cmd.trigger + " : " + cmd.description + "\n"
        msg += '---\n'
        msg += "For more info type '.help' followed by one of the available commands"
        return msg

    def help_with(self, cmd):
        if (idx := self._get_idx_of(cmd)) is None:
            return "I don't know about " + cmd
        msg = "" + cmd + ": "
        msg += self._commands[idx].description + "\n"
        if len(self._options[idx]) != 0:
            msg += "    Options:\n"
            for opt in self._options[idx]:
                msg += "        -" + opt.full + " (-" + opt.abrv + ") '" + opt.desc + "'\n"
        if len(self._flags[idx]) != 0:
            msg += "    Flags:\n"
            for flg in self._flags[idx]:
                msg += "        --" + flg.full + " (--" + flg.abrv + ") '" + flg.desc + "'\n"
        return msg
