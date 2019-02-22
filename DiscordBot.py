import asyncio
import os
from pathlib import Path
import sys

import discord  # As of Jan 2019 Discord.py needs python 3.5 or 3.6

from google_lib import search_results, print_search_results

import calculator

from config import (
    TEST_CHANNEL_ID,
    TOKEN,
)

client = discord.Client()


# ----- non asyncronis functions ------ #
# ------------------------------------- #


def count_members(unique=True):
    """Counts members across all servers."""
    if unique==True:
        members = set()
        for member in client.get_all_members():
            members.add(member)

        return len(members)
    else:
        members = int(0)
        for member in client.get_all_members():
            members += 1
        return members


def get_token():
    """Sets the bot's token to whatever is on the first line of TOKEN.txt
    
    Will create TOKEN.txt if it doesn't already exists for convenience
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
    try:
        print('attempting to list all channels...')
        n = 0
        for channel in client.get_all_channels():
            n += 1
            print(f'{n}: {channel.server} {Channel.position} {channel.type} {channel.id} {channel}')
        print(f'Found {n} channels')
    except:
        print('error: failed to list all channels {}')


def channel_lookup(channelid):
    """Finds a Discord.Client.Channel object by matching the ID"""
    for channel in client.get_all_channels():
        if channel.id == channelid:
            print(f'found channel with id={channelid}')
            return channel
        # else:
        #     print(f'failed to find channel with id={channelid}')


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
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(game=discord.Game(
        name=f'Serving {count_members()} unique members and {len(client.servers)} servers'))
    list_channels()
    channel_lookup('TEST_CHANNEL_ID')  # testing function
    # await spam("Patcha online")
    # while True:
    #     await client.get_message()


@client.event
async def get_messsage(message):
    content = message.content
    await spam(f"Received message: '{content}'")

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
        await spam(" ".join(results))
        # await client.send_message(
        #    destination=message.channel,
        #    content=" ".join(results),
        # )



@client.event
async def on_message(message):  # I think the func name has to be 'on_message'
    if message.content.startswith('!'):
        msg = 'You used the prefix "!" ... I current can not do anything though, sorry!'
        await client.send_message(message.channel, msg)


# ------- start the bot? ---------- #
# --------------------------------- #


if __name__ == "__main__":
    print(f'discord.py version {discord.__version__}')
    try:
        client.run(TOKEN)
    except discord.errors.LoginFailure:
        if not TOKEN:
            raise Exception("No token read")
        else: raise
