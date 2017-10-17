#!/usr/bin/env python3

import collections
import os
import re

import discord

BRIDGE_BOTS = {
    "irc": ("^\*\*<(?P<user>.*)>\*\* (?P<content>.*)$", "_irc")
}


def format_message(message):
    content = message.clean_content
    for o in message.embeds + message.attachments:
        if o["url"] not in content:
            content += "\n%s" % o["url"]

    user = message.author.name
    content = content.strip()

    if user in BRIDGE_BOTS:
        regex, postfix = BRIDGE_BOTS[user]
        match = re.match(regex, content)
        if match:
            user = match.group("user") + postfix
            content = match.group("content")

    return "[%s] <%s> %s\n" % (message.timestamp.strftime("%Y-%m-%d %H:%M:%S"), user, content)


def get_history(token, servers):
    os.makedirs("logs", exist_ok=True)
    client = discord.Client()

    @client.event
    async def on_ready():
        history = collections.defaultdict(list)

        for channel in client.private_channels:
            cid = "private.%s" % "_".join([x.name for x in channel.recipients])
            print("Fetching %s" % cid)
            async for message in client.logs_from(channel, limit=10000000):
                history[cid].append(message)

        for server in client.servers:
            if servers and server.name not in servers:
                continue

            for channel in server.channels:
                cid = "%s.%s" % (server.name, channel.name)
                print("Fetching %s" % cid)
                async for message in client.logs_from(channel, limit=10000000):
                    history[cid].append(message)

        for channel, messages in history.items():
            messages.sort(key=lambda x: x.timestamp)
            with open("logs/%s.txt" % channel, "w") as f:
                for message in messages:
                    f.write(format_message(message))

        client.loop.call_later(1, client.loop.stop)

    client.run(token, bot=False)


if __name__ == "__main__":
    get_history("YOUR_TOKEN", None)
