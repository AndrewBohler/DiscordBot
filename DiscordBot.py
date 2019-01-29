import asyncio
import os
import sys

import discord  # As of Jan 2019 Discord.py needs python 3.5 or 3.6
from google_lib import search_results, print_search_results

# you need to create TOKEN.txt with the bot token on first line
file = open('TOKEN.txt')
TOKEN = file.readline()
file.close()

client = discord.Client()
testChanID = '538573824271187999'  # developer test channel


# ----- non asyncronis functions -------#
# ------------------------------------- #


def list_channels():
    try:
        print('attempting to list all channels...')
        for channel in client.get_all_channels():
            print(channel)
    except:
        print('error: failed to list all channels')


def channel_lookup(channelid):
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
    list_channels()
    channel_lookup('testChanID')  # testing function
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
                await client.send_message(message.channel, 'Dont sleeping')

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

client.run(TOKEN)
client.connect()
