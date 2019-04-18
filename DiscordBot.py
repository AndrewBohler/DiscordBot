import asyncio
import logging

import discord

import config

TOKEN = config.TOKEN


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(f'discord.py version {discord.__version__}')
    client = MyClient()
    client.run(TOKEN)
