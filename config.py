import os
import sys

TEST_CHANNEL_ID = '538573824271187999'
try:
    TOKEN = os.environ['DISCORD_TOKEN']
except KeyError:
    sys.exit(
        'KeyError: DISCORD_TOKEN environment variable not set\n'
        'Linux: export DISCORD_TOKEN="Paste bot token instide quotes"\n'
        'Windows: set DISCORD_TOKEN=Paste bot token without quotes')
