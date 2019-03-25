import asyncio
from collections import deque
import re

import discord
from discord import utils

import config
import DiscordBot
import myclient

# COMMANDS = {
#     'spam': Spam()
# }


class Arg:
    """
    Single command-line style argument
    
    Properties
    ----------
    string : str
        the argument string
    type : int
        The interpreted type of argument

        0 unrecognized
        1 command: 'foo'
        2 short flag: '-f'
        3 long flag: '--flag'
        4 nested (double or single) quotes:
            'text symbols(!) commands or --flags'
    """
    def __init__(self, string: str):
        self.string = string
        self.type = None

        self._set_type()

    def _set_type(self):
        if self.string[0] in ('"', "'"):  # Quoted block
            self.type = 4
        elif self.string[:2] == '--':  # Long flag
            self.type = 3
        elif self.string[0] == '-':  # Short flag
            self.type = 2
        elif re.match(r'\w', self.string):  # Command (word)
            self.type = 1
        else:  # Anything else, eg non word characters like '!'
            self.type = 0
    
    def __repr__(self):
        return (self.__class__.__module__ + '.' +
        self.__class__.__qualname__ + f"('{self.string}')")

    def __str__(self):
        return self.string

    def __eq__(self, x):
        if type(x) is str:
            return x == self.string
        elif type(x) is int:
            return x == self.type
        elif isinstance(x, self.__class__):
            return x.string == self.string
        else:
            return False


class Command:
    """Carrier for commandline style arguments"""
    def __init__(self, message, prefix, client: myclient.Client):
        self.args = []
        self.prefix = prefix
        self.channel = None
        self.client = client
        self.command = None
        self.index = 0
        self.message = message
        self.options = {
            '--test': self.test(),
            '-t': self.test()
            }
        self._pattern = re.compile(r'''(\w+|--?\w+|'.*?'|".*?")''')
        self._issued_from = message.channel

        self._parse(message.content)
        for arg in self.args:
            if arg[1] in (2, 3):
                self.set_option(arg[0])
            else:
                break


    def _parse(self, msg: str):
        argList = re.findall(self._pattern, msg)
        for arg in argList:
            self.args.append(Arg(arg))


    def print(self, verbose=0):
        print(self._info(verbose))

    def _info(self, verbose=0) -> str:
        msg = ''
        if verbose == 0:
            return self.args
        elif verbose == 1:
            for arg in self.args:
                msg += arg
            return msg

    async def respond(self, msg: str):
        await self.client.send_message(self._issued_from, content=msg)

    def test(self):
        info = self._info()
        msg = '```\n' + self.message.content + '\n```'
        msg += ('`' + info + '`')
        asyncio.ensure_future(self.respond(msg))

    async def set_option(self, flag):
        if flag in self.options.keys():
            try:
                self.options[flag]
            except:
                print(f'Failed to set option "{flag}".')
        else:
            print(f'Failed to set option {flag}, option not found.')

    async def execute(self, index):
        for arg in self.args[index:]:
            if arg.type in (2, 3):
                pass
            elif arg.type == 1:
                pass
            else:
                break


class Spam:

    def __init__(self, command: Command, client, index=0):
        self.client = client
        self.loop = deque()
        self.flags = dict()
        self.targets = []
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
        pass

    async def _run_loop(self):
        remove = []
        for func in self.loop:
            try:
                func()
            except:
                self.loop.popleft()

    def execute(self, ctx, message):
        flags = []
        channel = None
        message = None
        single_quote = False
        double_quote = False
        for i, item in enumerate(message):
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


async def create(message: discord.message, prefix: str, client: discord.Client):
    command = Command(message, prefix, client)
    command.print()  # for testing purposes


