import asyncio
import re

import discord
from discord import utils

import DiscordBot

# COMMANDS = {
#     'spam': Spam()
# }

client = None


class Command:
    """Carrier for commandline style arguments"""
    def __init__(self, message: discord.message, prefix: str):
        self.prefix = prefix
        self.channel = None
        self.command = None
        self.args = None
        self._message = message
        self._pattern = re.compile(r'''(--?\w+)(?:\s(\w+|'.*?'|".*?"))?''')
        self._issued_from = message.channel

        self._parse(message.content)
        self.test()

    def _parse(self, msg: str):
        command = re.search(
            r'(?<=' + self.prefix + r')(\w+)', self._message.content)
        if command is not None:
            self.command = command[1]
        self.args = re.findall(self._pattern, self._message.content)

    def print(self):
        print(self._info)

    def _info(self, verbose=0) -> str:
        if verbose == 0:
            return f'Command: {self.command} | Arguments: {self.args}'
        else:
            return f'Command: {self.command} | Arguments: {self.args}'

    async def respond(self, msg: str):
        await client.send_message(self._issued_from, msg)

    def test(self):
        msg = '```\n' + self._message.content + '\n```'
        msg += self._info()
        asyncio.ensure_future(self.respond(msg))


class Spam:

    def __init__(self):
        self.loop = []
        # self.options = {
        #     '-c': lambda msg,
        #     '--channel': self._set_channel()
        #     }

    def _parse(self, ctx, msg):
        for i, arg in enumerate(msg):
            if arg[0] == '-':
                for f in self.flags.keys():
                    if arg == f:
                        self.flags[f]

    def _set_channel(self, ctx, msg, i) -> discord.Channel:
        utils.g
    async def _run_loop(self):
        remove = []
        for func in self.loop:
            try:
                func()
            except:
                self.loop.pop(len(self.loop))

    def execute(self, ctx, message):
        flags = []
        channel = None
        message = None
        single_quote = False
        double_quote = False
        for i, item in enumerate(msg):
            if single_quote:
                if item[-1] == "'":
                    single_quote = False
            elif double_quote:
                if item[-1] == '"':
                    double_quote = False
            elif item[0] == "'":
                single_quote = True
            elif item[0] == '"':
                double_quote = True

            elif item[0] == '-':
                flags.append((item, i))

        self.loop.append(tuple(channel, msg))

async def create(message: discord.message, prefix):
    command = Command(message, prefix)
    command.print()
    msg = '***So you think you can just ***' + command._message.content + '***?***'
    await client.send_message(command._message.channel, content=msg)
    await client.send_message(message.channel, content='(╯°□°）╯︵ ┻━┻')
