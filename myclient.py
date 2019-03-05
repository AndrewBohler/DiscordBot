
import asyncio
from collections import deque

from discord import Client as discordClient

import config


class Client(discordClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outbound_messages = deque()

        asyncio.ensure_future(self._send_message_loop())

    async def _send_message_loop(self):
        while True:
            if self.outbound_messages:
                sm = self.outbound_messages.popleft()
                await sm
            if len(self.outbound_messages) > 0:
                print(f'There are {len(self.outbound_messages)} outbound messages in queue.')
            await asyncio.sleep(config.RATE_LIMIT)

    async def send_message(self, destination, content=None, *, tts=False, embed=None):
        """Overwrite discord.Client.send_message so that messages are first
        queued, then sent using super().send_message()"""
        self.outbound_messages.append(
            super().send_message(
                destination, content=content, tts=tts, embed=embed
                )
            )
