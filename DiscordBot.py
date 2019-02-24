import asyncio
import logging
import os
from pathlib import Path
import sys

import discord
from google_lib import search_results, print_search_results

import calculator
import config

client = discord.Client()


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
    """Finds a Discord.Client.Channel object by matching the ID"""
    for channel in client.get_all_channels():
        if channel.id == channelid:
            print(f'found channel {channel.name} with id={channelid}')
            return channel
    print(f'failed to find channel with id={channelid}')

# ------- async functions -------- #
# -------------------------------- #


# async def


# ------- client events ---------- #
# -------------------------------- #

@client.event
async def spam(message: str) -> None:
    """Sends a message to all channels, use sparingly!"""
    for channel in client.get_all_channels():
        try:
            await client.send_message(
                destination=channel,
                content=message
            )
        except:
            pass


@client.event
async def on_ready():
    print('------------------------------------------------------')
    print(f'Logged in as: {client.user.name} id: {client.user.id}')
    print(f'shard {client.shard_id} of {client.shard_count}  ')
    print('------------------------------------------------------')
    await client.change_presence(
        game=discord.Game(name=serving_msg(), type=2))
    list_channels()
    channel_lookup(config.TEST_CHANNEL_ID)  # testing function


@client.event
async def get_messsage(message):
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
async def on_message(message):  # I think the func name has to be 'on_message'
    if message.content.startswith('!'):
        msg = f"sorry {message.content.split(' ')[0]} is not a command... "
        msg += "well, actually there aren't any commands right now..."
        await client.send_message(message.channel, msg)


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
