#!/usr/bin/env python3

from sys import stderr, exit
import json
import re

from asyncio import CancelledError
import discord
from entrypoint2 import entrypoint


def format_message(message, server_name, channel_name):
    content = message.clean_content
    for obj in message.embeds + message.attachments:
        if 'url' in obj and obj['url'] not in content:
            content += '\n' + obj['url']

    return json.dumps(
        {
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'server': server_name,
            'channel': channel_name,
            'user': message.author.name,
            'message': content.strip(),
        }
    )


@entrypoint
def main(token, server=[], channel=[], max_messages_per_channel=10000000):
    '''Download discord chat history as (streamed) json
    token: Your discord token
    server: Python regex(es) matching server names to be included. If none specified, all servers will be downloaded. PMs are assigned the server name "__private".
    channel: Python regex(es) matching channel names to be included. If none specified, all channels will be downloaded.
    max_messages_per_channel: Maximum number of messages to get per channel.
    '''

    server_re = [re.compile(s) for s in server]
    channel_re = [re.compile(c) for c in channel]

    client = discord.Client()

    async def download_channel(channel, server_name, channel_name):
        try:
            messages = []
            async for msg in client.logs_from(channel, limit=max_messages_per_channel):
                print(format_message(msg, server_name, channel_name))
        except RuntimeError:
            pass
        except Exception as ex:
            print(
                'Caught {} while processing channel {}'.format(repr(ex), channel_name), file=stderr
            )

    @client.event
    async def on_ready():
        channels = [
            (c, '_private', '_'.join(sorted([x.name for x in c.recipients])))
            for c in client.private_channels
        ]
        for server in client.servers:
            if server_re and [0 for re in server_re if re.match(server.name)]:
                continue
            channels += [(c, server.name, c.name) for c in server.channels]

        for c in channels:
            await download_channel(*c)

        client.loop.call_soon(exit)

    client.run(token, bot=False)
