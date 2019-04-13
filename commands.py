import asyncio
from collections import deque
import re

import discord
from discord import utils

import config
import DiscordBot
import myclient

COMMANDS = {}
PATTERN = re.compile(r'''('.*?'|".*?"|\S+)''')


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
        2 short flag: '-b' or '--bar'
        3 nested (double or single) quotes: 'anything inside quotes'
    """
    docstring = """
    Single command-line style argument
    
    Properties
    ----------
    string : str
        the argument string
    type : int
        The interpreted type of argument

        0 unrecognized
        1 command: 'foo'
        2 short flag: '-b' or '--bar'
        3 nested (double or single) quotes: 'anything inside quotes'
    """
    def __init__(self, string: str):
        self.string = string
        self.type = None

        self._set_type()

    def _set_type(self):
        if self.string[0] in ('"', "'"):  # Quoted block
            self.type = 3
        elif self.string[0] == '-':  # flag
            self.type = 2
        elif re.match(r'\w', self.string):  # Command (word)
            self.type = 1
        else:  # Unknown, e.g. arg starts with non-word characters like '!'
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


class ArgumentList:
    def __init__(self, string):
        self.args = [Arg(a) for a in re.findall(PATTERN, string)]
        self.string = string
        
    def __repr__(self):
        return (
            f"{self.__class__.__module__}.{self.__class__.__qualname__}" +
            f"('{self.string}')"
        )

    def __iter__(self):
        yield from self.args

    def __str__(self):
        return f'{[str(arg) for arg in self]}'


class Command:
    '''Subclass this to create custom commands.'''
    client = None  # set this after importing
    _commands = {}

    def __init__(
        self,
        caller=None,
        prefix='',
        message=None,
        *args, **kwargs
    ):
        self.args = ArgumentList(message.content)
        self.prefix = prefix
        self.caller = caller
        self.kwargs = kwargs

    @property
    def commands(self):
        return __class__._commands

    @classmethod
    def name(cls):
        return cls.__name__

    @staticmethod
    def load_commands():
        cmdlist = {
            c.__class__.__name__.lower(): c for c in __class__.__subclasses__}
        __class__._commands.clear()
        __class__._commands.update(cmdlist)

    @staticmethod
    def set_client(client):
        __class__.client = client

    def execute(self, *args, **kwargs):
        '''Called when a command is issued.'''
        raise NotImplementedError

    def __repr__(self):
        args = ', '.join(self.args)
        kwargs = ', '.join([f'{k}={v}' for k, v in self.kwargs.items()])
        return self.__qualname__ + f'({", ".join([args, kwargs])})'


class Test(Command):
    """Test command"""
    def execute(self):
        print('This is a test command!')
        print(f'args: {self.args}')
        print(f'kwargs: {self.kwargs}')
        self.client.send_message(self.message.channel, self.test_message)

    @property
    def test_message(self):
        msg = 'Command: `test`, '
        msg += f'you supplied {len(self.args)} arguments:\n'
        if self.args:
            for i, arg in enumerate(args):
                if i == 0:
                    msg += f'`{arg}`'
                else:
                    msg += f', `{arg}`'
        msg += '\nThank you for trying my bot.'
        return msg


class SubTest(Test):
    @property
    def test_message(self):
        msg = 'Sub command: Test, '
        msg += super().test_message


#  Considering writing a function as a command rather than a class.
#  Might be a better way to structure even if this changes back to a class.
async def spam(command, args: list, client=None):
    client = client
    target = None
    index = 0
    options = {
        '-t': set_target(),
        '--target': set_target,
        '-h': help(),
        '--help': help()
    }
    for arg in args:
        if arg.type in (2, 3):
            options[arg.string]
        elif arg.type == 1:
            raise TypeError
    
    def flags():
        "Methods for handling flags."
        def set_target():
            '''
            -t, --target
                |required| searches for "user" in server. If a exact match is found
                sets "user" as the target
            '''
            target = args[i+1]
            if not target.type == 1:
                raise ValueError('Target must be username in quotes')

        def set_channel():
            pass

    def commands():
        "Method containg all internal commands."
        def help():
            if args[index + 1]:
                send_message(
                    options[arg.string].__doc__
                )
            else:
                # msg ="\n".join([for flag in spam.flags.*: flag.__doc__])
                pass


class Spam:
    """Spams text in text channel"""
    def __init__(self, command, client=None, *args, **kwargs):
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


