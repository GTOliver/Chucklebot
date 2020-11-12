import discord


class Bot(discord.Client):
    def __init__(self, guild_name, channel_id, logger=None):
        """
        Bot for use with a single Discord Guild and Text Channel

        :param guild_name: The name of the Discord Guild to join
        :type guild_name: string

        :param channel_id: The ID of the channel to be active in
        :type channel_id: int

        :param logger: An optional logger to
        """
        super().__init__()
        self._main_guild_name = guild_name
        self._main_channel_id = channel_id
        self._logger = logger

        self.main_guild = None
        self.main_channel = None

        self._on_ready_msg = None
        self._message_handler = None

    def set_ready_message(self, msg):
        """ Set a message to be sent to the channel on connection

        :param msg: Message to be sent
        :type msg: string
        """
        self._on_ready_msg = msg

    def set_message_handler(self, handler):
        """ Set a handler to respond to Discord messages in the main channel.

        The handler must be an async function which takes a discord.Message.

        :param handler: The handler for message
        :type handler: An async function (discord.Message)
        """
        self._message_handler = handler

    async def on_ready(self):
        self._log_info("Connection Established")
        for guild in self.guilds:
            if guild.name == self._main_guild_name:
                self.main_guild = guild
        self.main_channel = self.main_guild.get_channel(self._main_channel_id)
        if msg := self._on_ready_msg:
            await self.send_message(msg)

    async def on_message(self, message):
        if message.channel.id == self._main_channel_id and not message.author.id == self.user.id:
            self._log_info("Received message in main channel. ID: {}".format(message.id))
            await self._message_handler(message)

    async def send_message(self, message):
        """ Send a message to the main channel

        :param message: The text to send to the server
        :type message: string
        """
        self._log_info("Sending message: {}".format(message))
        await self.main_channel.send(message)

    def _log_info(self, info):
        if self._logger:
            self._logger.log_message(info)
