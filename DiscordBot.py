import asyncio
import logging
import os
from pathlib import Path
import sys

import discord
from discord import utils, Status
from google_lib import search_results, print_search_results

import calculator
import commands
import config
import myclient

PREFIX = '!'

client = myclient.Client()
# terminal = Terminal()

# class Terminal:

#     def __init__(self):
#         self.run = False
    
#     async def run(self):
#         self.run = True
        

#     async def _loop():
#         while self.run is True:
#             await command = self._get_input()
#             await commands.create(command, PREFIX, terminal=True)
#     async def _get_input():
#         msg = input('<DiscordBot> ')




# ----- non asyncronis functions ------ #
# ------------------------------------- #


def count_members(unique=True) -> int:
    """Counts members across all servers."""
    if unique:
        members = set()
        for member in client.get_all_members():
            members.add(member)

        return len(members)
    else:
        members = int(0)
        for member in client.get_all_members():
            members += 1
        return members


def serving_msg() -> str:
    msg = '{} unique members in {} servers'.format(
        count_members(), len(client.servers))
    return msg


def get_token() -> str:
    """Depricated, probably should be removed now that the token is stored in
    an environment variable
    """
    try:
        with open('TOKEN.txt') as f:
            token = f.readline().strip()
            if token == '':
                raise Exception(
                    "'TOKEN.txt' is blank. Copy token into first line and run again")
            return token
    except FileNotFoundError:
        Path('TOKEN.txt', exist_ok=True).touch()
        raise FileNotFoundError(
            "Created 'TOKEN.txt'. Copy token into the first line and run again.")


def list_channels():
    """Prints a list of all channels, probably only useful for testing."""
    print('listing all channels...')
    print('|_{0:_^5}_|_{1:_^24}_|_{2:_^3}_|_{3:_^24}_|_{4:_^5}_|_{5:_^18}_|'.format(
            'num', 'server', 'pos', 'channel', 'type', 'channel id'))
    for i, channel in enumerate(client.get_all_channels()):
        print('| {0:5} | {1:24} | {2:3} | {3:24} | {4:>5} | {5:18} |'.format(
            i, channel.server.name, channel.position, channel.name,
            channel.type, channel.id))
    print(f'Found {i + 1} channels')


def channel_lookup(channelid):
    """Finds a discord.Client.Channel object by matching the ID"""
    for channel in client.get_all_channels():
        if channel.id == channelid:
            print(f'found channel "{channel.name}"" with id={channelid}')
            return channel
    print(f'failed to find channel with id={channelid}')


def find_user(server: discord.server, user: str) -> bool:
    member = utils.find(lambda m: m.name == user, server.members)
    return member


# ------- async functions -------- #
# -------------------------------- #

async def parse_args(args) -> (str, list, list):
    """converts a message into arguments and flags"""
    cmd = args.pop(0)
    flags = []
    for i, arg in enumerate(args):
        if arg[0] == '-':
            flags.append(args[i])
        else:
            args = args[i:]
    print('command: "{cmd}" flags: {flags} message: {args}')


# ------- client events ---------- #
# -------------------------------- #

@client.event
async def on_ready():
    print('------------------------------------------------------')
    print(f'Logged in as: {client.user.name} id: {client.user.id}')
    print(f'Shard #{client.shard_id} of {client.shard_count}')
    print('------------------------------------------------------')
    await client.change_presence(
        game=discord.Game(name=serving_msg(), type=2))
    list_channels()  # testing function
    channel_lookup(config.TEST_CHANNEL_ID)  # testing function


@client.event
async def get_messsage(message):  # From tutorial, only for reference
    content = message.content
    if content.startswith('test'):
        counter = 0
        tmp = await client.send_message(
            message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

                await client.edit_message(
                    tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif content.startswith('google'):
        search_string = content[len('google') + 1:]
        results = search_results(search_string, num_pages=1)
        await client.send_message(
           destination=message.channel,
           content=" ".join(results),
        )


@client.event
async def on_message(message):  # This is overwritting the default on_message()
    if message.content.startswith(PREFIX):
        asyncio.ensure_future(commands.create(message, PREFIX, client))

    else:
        pass


# ------- start the bot? ---------- #
# --------------------------------- #


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(f'discord.py version {discord.__version__}')
    try:
        client.run(config.TOKEN)
    except discord.errors.LoginFailure:
        if not config.TOKEN:
            raise Exception("No token read")
        else:
            raise
