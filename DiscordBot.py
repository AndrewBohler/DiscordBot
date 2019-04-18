import asyncio
import time
import logging

import discord
from discord.ext import commands

import config

TOKEN = config.TOKEN


class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged in as ', self.user)
        status_ticker = [
            f'{len(self.guilds)} guilds',
            f'{len([m for m in self.get_all_members()])} members',
            'life = 42',
            'I\'m dae queen',
            'for money!',
            'Honk! Honk!',
            'feelsbadman',
            'Git Gud',
            'with ur mom!'
        ]
        while True:
            for msg in status_ticker:
                await self.change_presence(activity=discord.Game(msg))
                await asyncio.sleep(5)

bot = MyBot(command_prefix='')

@bot.command()
async def joined(ctx):
    await ctx.send(f'{ctx.author} joined at {ctx.author.joined_at}')

@bot.command()
async def test(ctx):
    args = string_to_args(ctx.message.content)
    msg = '`' + '` `'.join(args) + '`'
    await ctx.send(msg)

def string_to_args(string: str, start=0, end=None):
    args = string.split(' ')
    if end is None or end > len(args) + 1:
        end = len(args) + 1
    return args[start:end]

@bot.command()
async def spam(ctx):
    ctx.send('Not Implimented')
    logging.info('bot.command(spam) not implimented.')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(f'discord.py version {discord.__version__}')
    bot.run(TOKEN)
