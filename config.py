import os
import sys

TEST_CHANNEL_ID = '538573824271187999'
RATE_LIMIT = 0.5  # discord rate limit (seconds between messages)
try:
    TOKEN = os.environ['DISCORD_TOKEN']
except KeyError:
    sys.exit(
        'KeyError: DISCORD_TOKEN environment variable not set\n'
        'Linux: export DISCORD_TOKEN="Paste bot token instide quotes"\n'
        'Windows: set DISCORD_TOKEN=Paste bot token without quotes')
